import cv2
import numpy as np
from django.http import HttpResponse
from .models import Request
from django.utils import timezone


def runtext(request):
    text = request.GET.get('text', 'Бегущая строка')

    Request.objects.create(text=text, timestamp=timezone.now())

    # Параметры видео
    width = 100
    height = 100
    fps = 60
    duration = 3

    # Создаем объект VideoWriter для записи видео
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    video = cv2.VideoWriter('output.mp4', fourcc, fps, (width, height))

    # Создаем черный фон
    background = np.zeros((height, width, 3), dtype=np.uint8)

    # Параметры текста
    font = cv2.FONT_HERSHEY_COMPLEX
    font_scale = 0.5
    thickness = 1
    text_size = cv2.getTextSize(text, font, font_scale, thickness)[0]

    # Начальная позиция текста
    x = width
    y = (height + text_size[1]) // 2

    # Вычисляем скорость движения строки
    text_width = text_size[0]
    total_frames = fps * duration
    speed = (width + text_width) / total_frames

    # Генерируем кадры видео
    for _ in range(total_frames):
        frame = background.copy()
        cv2.putText(frame, text, (int(x), y), font, font_scale, (255, 255, 255), thickness, cv2.LINE_AA)
        video.write(frame)

        # Перемещаем текст влево
        x -= speed
        if x < -text_width:
            x = width

    # Закрываем объект VideoWriter
    video.release()

    with open('output.mp4', 'rb') as file:
        response = HttpResponse(file.read(), content_type='video/mp4')
        response['Content-Disposition'] = 'attachment; filename="output.mp4"'
        return response
