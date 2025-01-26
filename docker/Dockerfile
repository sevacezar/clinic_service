# Базовый образ
FROM python:3.10.12-slim

# Переменные окружения
ENV PYTHONDONTWRITEBYTECODE 1  # Отключение создания pyc-файлов
ENV PYTHONUNBUDDERED 1  # Логирование без буферизации

# Установка рабочей директории
WORKDIR /app

# Копирование файла зависимостей
COPY ../requirements/requirements_prod.txt /app/requirements.txt
# Установка зависимостей
RUN pip install --upgrade pip -r /app/requirements.txt

# Копирование кодовой базы проекта
COPY .. /app

# Скрипт ожидания запуска БД перед запуском приложения, делаем исполняемым
RUN chmod +x /app/wait-for-it.sh

# Запуск команды по умолчанию (в docker-compose переопределяется)
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]