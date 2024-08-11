# drf_project

## Запуск проекта с использованием Docker

1. Убедитесь, что у вас установлены Docker и Docker Compose.

2. Клонируйте репозиторий:

```bash
git clone https://github.com/your-username/your-repo.git
cd your-repo
```

3. Создайте файл .env в корневой директории проекта и настройте переменные окружения.

4. Соберите и запустите контейнеры:

```bash
docker-compose up --build
```
5. Примените миграции:

```bash
docker-compose exec web python manage.py migrate
```
6. Проект будет доступен по адресу http://localhost:8000

## Остановка проекта

Для остановки проекта выполните:

```bash
docker-compose down
```