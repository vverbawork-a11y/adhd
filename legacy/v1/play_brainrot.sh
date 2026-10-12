#!/bin/bash
# Включаем подсветку
sudo pinctrl set 22 op dh

VIDEO_DIR="/home/pi/videos/ready"

while true; do
    if ls $VIDEO_DIR/*.raw 1> /dev/null 2>&1; then
        # Выбираем случайный файл
        RANDOM_VIDEO=$(ls $VIDEO_DIR/*.raw | shuf -n 1)
        echo "Looping: $RANDOM_VIDEO"
        
        # КРУТИМ ВЕЧНО (-stream_loop -1)
        ffmpeg -y -nostdin -stream_loop -1 -f rawvideo -pixel_format bgr565le -video_size 320x240 -r 60 -re -i "$RANDOM_VIDEO" -pix_fmt rgb565le -f fbdev /dev/fb1
    else
        echo "Waiting for videos..."
        sleep 5
    fi
done
