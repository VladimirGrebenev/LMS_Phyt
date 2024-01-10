# Learning Management System Phit

## Стек

- Python 3.10  
- Django==5.0.1
- djangorestframework==3.14.0
- and others in requirements.txt
- SQLite 3

## Запуск

1. Клонировать в IDE проект
2. Установить зависимости pip install requirements.txt
3. создать файл .env на основе .env_sample со своими настройками
4. наполнить для тестирования базу юззерами python manage.py fillusers 
   (теперь можно использовать например email админа для входа admin@mail.ru 
   и пароль admin)
5. запустить проект python manage.py runserver
6. перейти к изучению документации:
 - http://127.0.0.1:8000/swagger/
 - http://127.0.0.1:8000/redoc/
7. открыть в браузере список endpoints http://127.0.0.1:8000/
8. для тестов запускаем python manage.py test


## Лицензия

MIT