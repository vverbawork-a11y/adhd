"""Verify the scope processing contract; these are not display/ADC tests."""

from dataclasses import FrozenInstanceError
from threading import Barrier, Thread
import unittest

from tools.waveform_core import AudioRingBuffer, build_scope_frame, min_max_envelope


class AudioRingBufferTests(unittest.TestCase):
    def test_defaults_and_latest_bounded_window(self):
        ring = AudioRingBuffer(capacity_samples=4)
        self.assertEqual(ring.sample_rate, 48000)
        self.assertEqual(ring.append(value / 10 for value in range(10)), 10)
        snapshot = ring.snapshot()
        self.assertEqual(snapshot.samples, (0.6, 0.7, 0.8, 0.9))
        self.assertEqual(snapshot.end_sample, 10)
        self.assertEqual(snapshot.start_sample, 6)
        self.assertEqual(ring.snapshot(2).samples, (0.8, 0.9))
        self.assertEqual(ring.snapshot(100).samples, snapshot.samples)
        ring.append((-0.1, -0.2))
        self.assertEqual(ring.snapshot().samples, (0.8, 0.9, -0.1, -0.2))
        self.assertEqual(ring.snapshot().start_sample, 8)

    def test_invalid_batch_does_not_commit_its_valid_prefix(self):
        ring = AudioRingBuffer(capacity_samples=3)
        ring.append((0.2, 0.3))
        before = ring.snapshot()
        for invalid in (float("nan"), float("inf"), -float("inf"), 1.1, -1.1,
                        "0.1", True, None):
            with self.subTest(invalid=invalid):
                with self.assertRaises(ValueError):
                    ring.append((0.4, invalid))
                self.assertEqual(ring.snapshot(), before)

    def test_snapshot_is_immutable_and_independent_of_later_capture(self):
        ring = AudioRingBuffer(capacity_samples=2)
        ring.append((-1, 1))
        ring.set_jack_connected(True)
        snapshot = ring.snapshot()
        with self.assertRaises(FrozenInstanceError):
            snapshot.jack_connected = False
        with self.assertRaises(TypeError):
            snapshot.samples[0] = 0
        ring.append((0, 0))
        ring.set_jack_connected(False)
        self.assertEqual(snapshot.samples, (-1, 1))
        self.assertTrue(snapshot.jack_connected)
        self.assertFalse(ring.snapshot().jack_connected)

    def test_connection_flag_does_not_depend_on_silence(self):
        ring = AudioRingBuffer()
        ring.append([0] * 800)
        ring.set_jack_connected(True)
        frame = build_scope_frame(ring.snapshot(), align_trigger=True)
        self.assertTrue(frame.jack_connected)
        self.assertFalse(frame.triggered)
        self.assertEqual(frame.envelope, ((0.0, 0.0),) * 320)
        ring.set_jack_connected(False)
        self.assertFalse(build_scope_frame(ring.snapshot()).jack_connected)

    def test_invalid_configuration(self):
        for value in (0, -1, 1.5, True):
            with self.subTest(value=value):
                with self.assertRaises(ValueError):
                    AudioRingBuffer(sample_rate=value)
                with self.assertRaises(ValueError):
                    AudioRingBuffer(capacity_samples=value)
                with self.assertRaises(ValueError):
                    AudioRingBuffer().snapshot(value)
        with self.assertRaises(ValueError):
            AudioRingBuffer().set_jack_connected(1)

    def test_capture_and_snapshot_share_complete_batches(self):
        capacity = 7
        ring = AudioRingBuffer(capacity_samples=capacity)
        barrier = Barrier(2, timeout=5)
        errors = []

        def capture():
            try:
                for index in range(200):
                    barrier.wait()
                    ring.append([index % 2] * capacity)
                    barrier.wait()
            except BaseException as error:
                errors.append(error)
                barrier.abort()

        thread = Thread(target=capture, daemon=True)
        thread.start()
        snapshots = []
        try:
            for _ in range(200):
                barrier.wait()
                snapshots.append(ring.snapshot())
                barrier.wait()
        except BaseException:
            barrier.abort()
            raise
        finally:
            thread.join(timeout=5)
            if thread.is_alive():
                barrier.abort()
                thread.join(timeout=1)
        self.assertFalse(thread.is_alive())
        self.assertEqual(errors, [])
        for snapshot in snapshots:
            self.assertEqual(snapshot.end_sample % capacity, 0)
            self.assertIn(len(snapshot.samples), (0, capacity))
            if snapshot.samples:
                expected = (snapshot.end_sample // capacity - 1) % 2
                self.assertEqual(snapshot.samples, (expected,) * capacity)


class ScopeProcessingTests(unittest.TestCase):
    def test_envelope_preserves_both_polarities_of_single_sample_peaks(self):
        samples = [0] * 13
        samples[3], samples[8] = 1, -1
        envelope = min_max_envelope(samples, 3)
        self.assertEqual(envelope, ((0.0, 1.0), (0.0, 0.0), (-1.0, 0.0)))

    def test_uneven_bins_keep_last_sample_and_small_inputs_repeat(self):
        self.assertEqual(min_max_envelope((0, 0, 0, 0, 1), 2),
                         ((0.0, 0.0), (0.0, 1.0)))
        self.assertEqual(min_max_envelope((-1, 1), 4),
                         ((-1.0, -1.0), (-1.0, -1.0), (1.0, 1.0), (1.0, 1.0)))
        self.assertEqual(min_max_envelope((), 320), ())

    def test_latest_window_reports_absolute_sample_position(self):
        ring = AudioRingBuffer(capacity_samples=8)
        ring.append([0] * 12)
        frame = build_scope_frame(ring.snapshot(), columns=3, window_samples=5)
        self.assertEqual(frame.start_sample, 7)
        self.assertEqual(frame.sample_count, 5)
        self.assertFalse(frame.triggered)

    def test_rising_trigger_keeps_phase_as_capture_moves_forward(self):
        period = (-1, -0.5, -0.1, 0, 0.1, 0.5, 1, 0.5)
        ring = AudioRingBuffer(capacity_samples=64)
        ring.append(period * 3)
        first = build_scope_frame(ring.snapshot(), columns=6, window_samples=6,
                                  align_trigger=True)
        self.assertTrue(first.triggered)
        self.assertEqual(first.start_sample, 11)
        self.assertEqual(first.envelope[0], (0.0, 0.0))
        ring.append(period[:2])
        second = build_scope_frame(ring.snapshot(), columns=6, window_samples=6,
                                   align_trigger=True)
        self.assertTrue(second.triggered)
        self.assertEqual(second.start_sample, 19)
        self.assertEqual(second.envelope, first.envelope)

    def test_hysteresis_rejects_small_crossings_and_uses_latest_window(self):
        ring = AudioRingBuffer(capacity_samples=32)
        ring.append((-0.005, 0.005) * 8)
        frame = build_scope_frame(ring.snapshot(), columns=4, window_samples=4,
                                  align_trigger=True, trigger_hysteresis=0.02)
        self.assertFalse(frame.triggered)
        self.assertEqual(frame.start_sample, 12)

    def test_trigger_requires_positive_excursion_and_complete_window(self):
        ring = AudioRingBuffer(capacity_samples=16)
        ring.append((-0.1, -0.005, 0.005, -0.005, 0.005))
        self.assertFalse(build_scope_frame(ring.snapshot(), window_samples=3,
                                          align_trigger=True).triggered)
        ring.append((0.1,))
        # The now-qualified crossing is too late for a complete three-sample window.
        self.assertFalse(build_scope_frame(ring.snapshot(), window_samples=3,
                                          align_trigger=True).triggered)
        ring.append((0.2,))
        self.assertTrue(build_scope_frame(ring.snapshot(), window_samples=3,
                                         align_trigger=True).triggered)

    def test_empty_buffer_and_invalid_processing_parameters(self):
        snapshot = AudioRingBuffer().snapshot()
        frame = build_scope_frame(snapshot)
        self.assertEqual(frame.envelope, ())
        self.assertEqual(frame.sample_count, 0)
        for parameters in ({"columns": 0}, {"window_samples": 0},
                           {"align_trigger": 1}, {"trigger_level": float("nan")},
                           {"trigger_hysteresis": -0.1},
                           {"trigger_level": 0.99, "trigger_hysteresis": 0.02}):
            with self.subTest(parameters=parameters):
                with self.assertRaises(ValueError):
                    build_scope_frame(snapshot, **parameters)
        with self.assertRaises(ValueError):
            min_max_envelope((0, float("nan")), 1)


if __name__ == "__main__":
    unittest.main()
