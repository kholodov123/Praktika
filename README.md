# Информационная система для автоматизации работы кинотеатра
Создание venv.
```sh
python -m venv venv
```
Активация venv.
```sh
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
venv\Scripts\Activate.ps1
```
Установка пакетов.
```sh
python -m pip install -r requirements.txt
```
Запуск сервера.
```sh
python manage.py runserver
```
URL сервера.
```sh
http://127.0.0.1:8000/
```
Данные суперпользователя.
```sh
Логин: kholodov
Пароль: 1
```
