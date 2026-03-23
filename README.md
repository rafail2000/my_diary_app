# The my diary app.

Веб-приложение для ведения личного дневника. Приложение позволяет пользователям создавать, редактировать и удалять
записи в дневнике, а также просматривать свои записи в удобном интерфейсе.

# Клонируйте репозиторий
git clone https://github.com/yourusername/my_diary.git /app

# Скопируйте .env.prod в .env
cp .env.prod /app/.env

# Запустите приложение
cd /app
docker-compose up -d

# Выполните миграции
docker-compose exec web python manage.py migrate

# Создайте суперпользователя
docker-compose exec web python manage.py csu