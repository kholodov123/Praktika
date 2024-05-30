# Информационная система для автоматизации работы кинотеатра
<b>Запуск</b><br>
• <code>python -m venv venv</code><br>
• <code>Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser</code><br>
• <code>venv\Scripts\Activate.ps1</code><br>
• <code>python -m pip install -r requirements.txt</code><br>
• <code>python manage.py runserver</code><br>
• <code>http://127.0.0.1:8000/</code><br>
<br>
<b>Если не прогружаются стили/фото</b><br>
```sh
python manage.py collectstatic
```
Данные суперпользователя.
```sh
Логин: kholodov
Пароль: 1
```
