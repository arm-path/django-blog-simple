### Начало работы:
#### 1. Настроить электронную почту smtp: 
Файл dj_project/settings.py:\
   1.1. Адрес электронной почты: EMAIL_HOST_USER\
   1.2. Пароль электронной почты: EMAIL_HOST_PASSWORD

#### 2. Установить зависимости:
>pip install -r requirements.txt
#### 3. Запустить Redis:
> docker-compose up
#### 4. Запустить Celery:
> celery -A dj_project worker -P eventlet
#### 5. Применить миграции и создать пользователя:
> python manage.py makemigrations \
> python manage.py migrate \
> python manage.py createsuperuser
### 6. Запустить Django.
> python manage.py runserver
celery -A proj worker -P eventlet

### Прочее:
[Внешний вид сайта](IMAGES)
