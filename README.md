# specialized-project-backend
Technology:
    Frontend: HTML + CSS + JS + Bootstrap5
    Backend: Django
    Database: Postgres
    ML-modeling: PyTorch

Инструменты
- Visual Studio
- DBeaver


Создание базы данных (Linux):

1. Скачиваем postgresql
sudo apt-get update
sudo apt-get install postgresql

2. Заходим в систему под суперпользователем
sudo -u postgres psql

3. Создаем пользователя и базу данных 
CREATE USER specuser WITH PASSWORD '12345678';
CREATE DATABASE specdatabase;
GRANT ALL PRIVILEGES ON DATABASE specdatabase TO specuser;

4. sudo service postgresql start

