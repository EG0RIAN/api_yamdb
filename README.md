# Проект YaMDb

Проект **YaMDb** собирает отзывы пользователей на произведения. Сами произведения в **YaMDb** не хранятся, здесь нельзя посмотреть фильм или послушать музыку.

# Как запустить проект:
Клонировать репозиторий и перейти в него в командной строке:

`git clone https://github.com/EG0RIAN/api_yamdb.git`

`cd api_yamdb`

Создать и активировать виртуальное окружение:

`python -m venv venv`

`source venv/bin/activate`

Установить зависимости из файла requirements.txt:

`python -m pip install --upgrade pip`

`pip install -r requirements.txt`

Выполнить миграции:

`python manage.py migrate`

Запустить проект:

`python manage.py runserver`

# Где Можно Посмотреть на примеры запросов к API ?
Например, после запуска проекта можно посмотреть [Документацию](http://127.0.0.1:8000/redoc/).

# Основные запросы
POST http://127.0.0.1:8000/api/v1/auth/signup/  
<sub>Регистрация Пользователя </sub>

    {
        "username":"Fake",
        "email": "Fake.fake@gmail.com"
    }

POST http://127.0.0.1:8000/api/v1/auth/token/        
в бэк приходит письмо с кодом  
<sub>Получение Jwt Токена</sub>

    {
        "username":"Fake",
        "confirmation_code": "biv4hr-69c31c5b2ad53627baf8c1f5273156e3"
    }

POST http://127.0.0.1:8000/api/v1/titles/1/reviews/1/comments/1/ 
<sub>Оставить комментарий для</sub>  
<sub>произведения с id=1</sub>  
<sub>ревью id=1</sub>  
<sub>Коммента id=1</sub>  

    {
        "text": "testComment"
    }

POST http://127.0.0.1:8000/api/v1/auth/users/me/
в бэк приходит письмо с кодом  
<sub>Получение Jwt Токена</sub>

    {
        "username": "Fake",
        "email": "Fake.fake@fake.com",
        "first_name": "",
        "last_name": "",
        "bio": "",
        "role": "user"
    }

# Над проектом работали

[Архипцев Егор](https://github.com/EG0RIAN)
[Григорий Кононихин](https://github.com/ddk-ops)
[Роман Демчак](https://github.com/JuniorRF/)