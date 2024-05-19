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
<<<<<<< HEAD
Если не прогружаются стили/фото.
```sh
python manage.py collectstatic
=======
Данные суперпользователя.
```sh
Логин: kholodov
Пароль: 1
>>>>>>> 4749ed49f2ef7638d54a87ae56451c112b351961
```
