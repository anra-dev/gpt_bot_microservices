FROM python:3.12

# Устанавливаем зависимости из requirements.txt
COPY requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r /app/requirements.txt

# Копируем исходный код из директории src
COPY src /app

# Указываем рабочую директорию
WORKDIR /app

# Запускаем команду для создания базы данных
RUN python models.py

# Запускаем приложение
CMD ["python", "main.py"]
