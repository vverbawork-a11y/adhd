#!/bin/bash
# 1. Включаем подсветку экрана 2.8 дюйма (пин 22)
/usr/bin/pinctrl set 22 op dh

# 2. Небольшая пауза, чтобы диск успел проснуться
sleep 3

# 3. Указываем папку с твоими аномалиями
DIR="/home/pi/videos/ready"

# 4. Проверяем, есть ли там .raw файлы
shopt -s nullglob
FILES=("$DIR"/*.raw)

if [ ${#FILES[@]} -gt 0 ]; then
    # Выбираем случайный файл
    RANDOM_VIDEO="${FILES[RANDOM % ${#FILES[@]}]}"
    echo "Starting: $RANDOM_VIDEO"
    # Запуск бесконечного цикла
    /usr/bin/ffmpeg -re -stream_loop -1 -f rawvideo -pixel_format rgb565le -video_size 320x240 -i "$RANDOM_VIDEO" -f fbdev /dev/fb1
else
    echo "No raw files found in $DIR"
    exit 1
fi
