"""Bounded mono-audio processing for a future oscilloscope overlay.

An ADC adapter must supply normalized samples in [-1, 1] at the declared
sample rate, and report the jack's physical connection independently. This
module captures no hardware and draws no pixels; it cannot verify display
refresh, flicker, or end-to-end latency.
"""

from collections import deque
from dataclasses import dataclass
import math
from numbers import Real
from threading import Lock
from typing import Iterable, Sequence


def _positive_int(value: int, name: str) -> int:
    if isinstance(value, bool) or not isinstance(value, int) or value <= 0:
        raise ValueError(f"{name} must be a positive integer")
    return value


def _sample(value: Real) -> float:
    if isinstance(value, bool) or not isinstance(value, Real):
        raise ValueError("samples must be real numbers")
    value = float(value)
    if not math.isfinite(value) or not -1.0 <= value <= 1.0:
        raise ValueError("samples must be finite and normalized to [-1, 1]")
    return value


@dataclass(frozen=True)
class AudioSnapshot:
    sample_rate: int
    samples: tuple[float, ...]
    jack_connected: bool
    end_sample: int

    @property
    def start_sample(self) -> int:
        """Absolute index of the first retained sample, starting from zero."""
        return self.end_sample - len(self.samples)


class AudioRingBuffer:
    """Commit complete capture batches and copy coherent, immutable snapshots.

    The default retains 100 ms at 48 kHz. Batch validation uses another
    capacity-limited deque, so a large batch does not grow temporary memory
    with its length. An invalid batch leaves both audio and counters unchanged.
    """

    def __init__(self, sample_rate: int = 48000, capacity_samples: int = 4800):
        self._sample_rate = _positive_int(sample_rate, "sample_rate")
        self._capacity = _positive_int(capacity_samples, "capacity_samples")
        self._samples: deque[float] = deque(maxlen=self._capacity)
        self._end_sample = 0
        self._jack_connected = False
        self._lock = Lock()

    @property
    def sample_rate(self) -> int:
        return self._sample_rate

    @property
    def capacity_samples(self) -> int:
        return self._capacity

    def append(self, samples: Iterable[Real]) -> int:
        """Append one complete valid batch; return its original sample count."""
        batch: deque[float] = deque(maxlen=self._capacity)
        count = 0
        for value in samples:
            batch.append(_sample(value))
            count += 1
        with self._lock:
            self._samples.extend(batch)
            self._end_sample += count
        return count

    def set_jack_connected(self, connected: bool) -> None:
        """Use physical jack detection; silence is still a connected input."""
        if not isinstance(connected, bool):
            raise ValueError("connected must be a boolean")
        with self._lock:
            self._jack_connected = connected

    def snapshot(self, window_samples: int | None = None) -> AudioSnapshot:
        """Return the latest available samples, capped by buffer capacity."""
        if window_samples is not None:
            _positive_int(window_samples, "window_samples")
        with self._lock:
            samples = tuple(self._samples)
            if window_samples is not None:
                samples = samples[-window_samples:]
            return AudioSnapshot(
                self._sample_rate, samples, self._jack_connected, self._end_sample
            )


def min_max_envelope(
    samples: Sequence[Real], columns: int
) -> tuple[tuple[float, float], ...]:
    """Return (minimum, maximum) per column without dropping narrow peaks.

    Every input sample belongs to a bin. With fewer samples than columns,
    samples repeat into adjacent columns; an empty input produces no bins.
    """
    _positive_int(columns, "columns")
    count = len(samples)
    if count == 0:
        return ()
    result = []
    for column in range(columns):
        start = column * count // columns
        end = max(start + 1, (column + 1) * count // columns)
        low = high = _sample(samples[start])
        for index in range(start + 1, end):
            value = _sample(samples[index])
            low = min(low, value)
            high = max(high, value)
        result.append((low, high))
    return tuple(result)


def _rising_start(
    samples: tuple[float, ...], window_samples: int,
    level: float, hysteresis: float,
) -> int | None:
    """Find the latest qualified rising crossing with a complete window."""
    latest_start = len(samples) - window_samples
    if latest_start < 1:
        return None
    low, high = level - hysteresis, level + hysteresis
    armed = False
    crossing = latest_crossing = None
    previous = samples[0]
    for index, value in enumerate(samples):
        if value <= low:
            armed = True
            crossing = None
        if armed and previous < level <= value:
            crossing = index
        if armed and crossing is not None and value >= high:
            if crossing <= latest_start:
                latest_crossing = crossing
            armed = False
            crossing = None
        previous = value
    return latest_crossing


@dataclass(frozen=True)
class ScopeFrame:
    """Processing result, ready for a separate display/compositor adapter."""

    sample_rate: int
    jack_connected: bool
    start_sample: int
    sample_count: int
    triggered: bool
    envelope: tuple[tuple[float, float], ...]


def build_scope_frame(
    snapshot: AudioSnapshot, *, columns: int = 320,
    window_samples: int = 800, align_trigger: bool = False,
    trigger_level: Real = 0.0, trigger_hysteresis: Real = 0.02,
) -> ScopeFrame:
    """Reduce a snapshot to a waveform, optionally aligned to a rising edge.

    Keep more than one window in the snapshot for triggering. A crossing must
    start below level minus hysteresis and reach level plus hysteresis. If no
    complete qualified window exists, use the latest window. The connection
    flag never depends on signal amplitude, and processing continues while
    disconnected so the display adapter can decide whether to draw the layer.
    """
    _positive_int(columns, "columns")
    _positive_int(window_samples, "window_samples")
    if not isinstance(align_trigger, bool):
        raise ValueError("align_trigger must be a boolean")
    level = _sample(trigger_level)
    hysteresis = _sample(trigger_hysteresis)
    if hysteresis < 0 or level - hysteresis < -1 or level + hysteresis > 1:
        raise ValueError("trigger hysteresis must fit inside [-1, 1]")
    start = max(0, len(snapshot.samples) - window_samples)
    triggered = False
    if align_trigger:
        crossing = _rising_start(snapshot.samples, window_samples, level, hysteresis)
        if crossing is not None:
            start = crossing
            triggered = True
    samples = snapshot.samples[start:start + window_samples]
    return ScopeFrame(
        sample_rate=snapshot.sample_rate,
        jack_connected=snapshot.jack_connected,
        start_sample=snapshot.start_sample + start,
        sample_count=len(samples),
        triggered=triggered,
        envelope=min_max_envelope(samples, columns),
    )
