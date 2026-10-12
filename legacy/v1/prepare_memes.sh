#!/bin/bash
FOLDER="$HOME/videos"
# Создаем папку для готовых видео, если её нет
mkdir -p "$FOLDER/ready"

for f in "$FOLDER"/*.mp4; do
    # Берем имя файла без расширения
    name=$(basename "$f" .mp4)
    echo "Processing $name..."
    # Конвертируем в быстрый RAW формат (30 FPS, поворот, обрезка под 2.8")
    ffmpeg -i "$f" -vf "transpose=1,fps=30,scale=320:240:force_original_aspect_ratio=increase,crop=320:240,format=rgb565le" -c:v rawvideo -f rawvideo -y "$FOLDER/ready/$name.raw"
done
echo "DONE! All videos are ready for brainrot."
