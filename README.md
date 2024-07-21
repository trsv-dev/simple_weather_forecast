# Simple weather forecast

### Прогноз погоды
![weather_forecast_screenshot.png](weather_forecast_screenshot.png)
## Описание
**Тестовое задание на позицию Junior Python Developer.**

Демо: http://forecast.trsv-dev.ru

Сделать web приложение, оно же сайт, где пользователь вводит название города, 
и получает прогноз погоды в этом городе на ближайшее время.

 - Вывод данных (прогноза погоды) должен быть в удобно читаемом формате.
 - Веб фреймворк можно использовать любой.
 - api для погоды: https://open-meteo.com/ (можно использовать какое-нибудь другое, 
если вам удобнее)

Будет плюсом если:

- написаны тесты,
- всё это помещено в docker контейнер,
- сделаны автодополнение (подсказки) при вводе города,
- при повторном посещении сайта будет предложено посмотреть погоду в городе, 
в котором пользователь уже смотрел ранее,

- ~~будет сохраняться история поиска для каждого пользователя, и будет API, показывающее сколько раз вводили какой город~~

## Стек технологий:
* Python==3.12
* Django==4.2.14
* pytest-django==4.8.0

## Запуск проекта

<details>

<summary>Инструкция по запуску в режиме локальной разработки</summary>

### **_Запуск из консоли._**

Клонируйте репозиторий с **develop веткой** к себе на машину:
```
git@github.com:trsv-dev/simple_weather_forecast.git
```
Перейдите в папку проекта:
```
cd simple_weather_forecast/
```
Установите виртуальное окружение (**если работаете в Linux**):
```
python3.12 -m venv venv
```
Активируйте виртуальное окружение:
```
source venv/bin/activate
```
Перейдите в папку **backend**:
```
cd backend/
```
Переименуйте **.env.example** в **.env**, ознакомьтесь с содержимым, внесите
необходимые изменения.

Установите зависимости из файла requirements.txt:
```
pip install -r requirements.txt
``` 
Создайте и примените миграции БД:
```
python manage.py makemigrations
python manage.py migrate
```
Создайте суперпользователя:
```
python manage.py createsuperuser
```
Запустите локальный сервер разработки:
```
python manage.py runserver 127.0.0.1:8000
```
Сайт будет доступен по адресу http://127.0.0.1:8000/,
админка будет доступна по адресу http://127.0.0.1:8000/admin/.

</details>

<details>

<summary>Инструкция по запуску в Docker-контейнерах</summary>

### **_Запуск в контейнерах._**

Клонируйте репозиторий с **develop веткой** к себе на машину:
```
git@github.com:trsv-dev/simple_weather_forecast.git
```
Перейдите в папку проекта:
```
cd simple_weather_forecast/
```

Переименуйте **.env.example** в **.env**, ознакомьтесь с содержимым, внесите
необходимые изменения.


Запустите контейнер в фоновом режиме:
```
docker compose -f docker-compose.yml up -d
```
Выполните и примените миграции БД (выполнять последовательно):
```
docker compose -f docker-compose.yml exec backend python manage.py makemigrations
docker compose -f docker-compose.yml exec backend python manage.py migrate
```
Соберите и скопируйте статику (выполнять последовательно):
```
docker compose -f docker-compose.yml exec backend python manage.py collectstatic
docker compose -f docker-compose.yml exec backend cp -r /app/collected_static/. /app/static/
```
Создайте суперпользователя:
```
docker compose -f docker-compose.yml exec backend python manage.py createsuperuser
```
Сайт будет доступен по адресу http://127.0.0.1:8000/,
админка будет доступна по адресу http://127.0.0.1:8000/admin/.

</details>

