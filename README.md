# Foodgram - социальная сеть для размещение фотографий котиков.
---

## Описание проекта
Мой финальный проект в рамках учебного курса по Python от Яндекс.Практикум. Foodgram - «Продуктовый помощник».
Пользователи могут регистрироваться, загружать фотографии своих любимых рецептов с подробным описанием,
отмечать понравившиеся рецепты и авторов, а так же скачать список покупок что бы ничего ен забыть!

Ознакомиться можно по ссылке: https://foodgram-varya.ddns.net/
Доступ к API через: https://foodgram-varya.ddns.net/api/
Подробная документация: https://foodgram-varya.ddns.net/api/docs/

## Стек технологий
- python 3.9 https://docs.python.org/3.9/
- Django  3.2 https://docs.djangoproject.com/en/3.2/
- djangorestframework  3.12.4 https://www.django-rest-framework.org/
- djoser  2.1.0 https://djoser.readthedocs.io/en/latest/index.html
- Pillow  9.0.0 https://pillow.readthedocs.io/
- fpdf2  2.7.6 https://py-pdf.github.io/fpdf2/index.html
- django-admin-list-filter-dropdown 1.0.3 https://pypi.org/project/django-admin-list-filter-dropdown/

## Локальный запуск backend
### Как запустить проект:

Клонировать репозиторий и перейти в него в командной строке:


```
cd backend 

python3 -m venv env 

```

* Если у вас Linux/macOS

    ```
    source env/bin/activate
    ```

* Если у вас windows

    ```
    source env/scripts/activate
    ```

```
python3 -m pip install --upgrade pip 

pip install -r requirements.txt 

python3 manage.py migrate 

python3 manage.py runserver
```

## Для развёртывания на удалённном сервере  
## Docker
Установка докера на компьютер
```
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh ./get-docker.sh
```
Загрузить на сервер новый конфиг для Docker Compose и запустить контейнеры.  
Создайте деррикторию проекта, скопируйте туда папку  `infra`  
Запустите контейнер в режиме демона, соберите статику и выполните миграции 
```
sudo docker compose -f docker-compose.production.yml up -d
docker compose -f docker-compose.production.yml exec backend python manage.py migrate
docker compose -f docker-compose.production.yml exec backend python manage.py collectstatic
docker compose -f docker-compose.production.yml exec backend cp -r /app/collected_static/. /backend_static/static/
``` 
### Nginx
Настроить «внешний» Nginx — тот, что вне контейнера — для работы с приложением в контейнерах.  
Откройте конфиг Nginx `nano /etc/nginx/sites-enabled/default` и укжите:
```
    location / {
        proxy_set_header        Host $host;
        proxy_set_header        X-Real-IP $remote_addr;
        proxy_set_header        X-Forwarded-Proto $scheme;
        proxy_pass              http://127.0.0.1:здесь_указать_порт_контейнера_nginx;
```
Перезагрузите конфиг Nginx:
```
sudo service nginx reload
```
## Примеры запросов к API

Начните с регистрации что бы получить доступ ко всем возможностям нашего проекта
Регистрация(POST) 
https://foodgram-varya.ddns.net/api/users/
```
# Пример запроса:
{
    "email": "vpupkin@yandex.ru",
    "username": "vasya.pupkin",
    "first_name": "Вася",
    "last_name": "Пупкин",
    "password": "Qwerty123"
}
# Ответ
{
    "email": "vpupkin@yandex.ru",
    "id": 0,
    "username": "vasya.pupkin",
    "first_name": "Вася",
    "last_name": "Пупкин"
}
```
Ознакомьтесь со всеми рецептами пользователей или заинтересовавшим Вас(GET)  
https://foodgram-varya.ddns.net/api/recipes/
https://foodgram-varya.ddns.net/api/recipes/1/

```
# Ответ
{
  "id": 0,
  "tags": [
    {
      "id": 0,
      "name": "Завтрак",
      "color": "#E26C2D",
      "slug": "breakfast"
    }
  ],
  "author": {
    "email": "user@example.com",
    "id": 0,
    "username": "string",
    "first_name": "Вася",
    "last_name": "Пупкин",
    "is_subscribed": false
  },
  "ingredients": [
    {
      "id": 0,
      "name": "Картофель отварной",
      "measurement_unit": "г",
      "amount": 1
    }
  ],
  "is_favorited": true,
  "is_in_shopping_cart": true,
  "name": "string",
  "image": "http://foodgram.example.org/media/recipes/images/image.jpeg",
  "text": "string",
  "cooking_time": 1
}
```
Добавьте понравившиеся рецепты в список покупок и скачайте его в удобном формате когда соберётесь за покупками
https://foodgram-varya.ddns.net/api/recipes/{id}/shopping_cart/
https://foodgram-varya.ddns.net/api/recipes/download_shopping_cart/

## Об авторе
Автор проекта: Бандуро Варя, ЯндексПрактикум.