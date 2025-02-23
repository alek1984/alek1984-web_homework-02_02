# Используем официальный облегчённый образ Python 3.11.9
FROM python:3.11.9-slim

# Устанавливаем рабочую директорию внутри контейнера
WORKDIR /app

# Копируем все файлы проекта в контейнер
COPY . /app

# Устанавливаем Poetry для управления зависимостями
RUN pip install --no-cache-dir poetry && \ 
    # Отключаем создание виртуального окружения внутри Poetry
    poetry config virtualenvs.create false && \ 
    # Устанавливаем все зависимости, указанные в pyproject.toml
    poetry install --no-interaction --no-ansi

# Определяем команду запуска приложения по умолчанию
ENTRYPOINT ["python", "main.py"]
