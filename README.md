# drf_project

## ������ ������� � �������������� Docker

1. ���������, ��� � ��� ����������� Docker � Docker Compose.

2. ���������� �����������:

```bash
git clone https://github.com/your-username/your-repo.git
cd your-repo
```

3. �������� ���� .env � �������� ���������� ������� � ��������� ���������� ���������.

4. �������� � ��������� ����������:

```bash
docker-compose up --build
```
5. ��������� ��������:

```bash
docker-compose exec web python manage.py migrate
```
6. ������ ����� �������� �� ������ http://localhost:8000

## ��������� �������

��� ��������� ������� ���������:

```bash
docker-compose down
```