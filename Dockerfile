# Используем официальный Python-образ
FROM python:3.11


# Указываем рабочую директорию внутри контейнера
WORKDIR /Nest

# Копируем файл зависимостей в контейнер
COPY requirements.txt .

# Устанавливаем зависимости
RUN pip install --no-cache-dir -r requirements.txt

# Копируем всё содержимое проекта в рабочую директорию контейнера
COPY . .

# Указываем, что по умолчанию будет запускаться контейнер с Django
CMD ["python manage.py runserver 0.0.0.0:8080"]