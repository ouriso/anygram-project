# Anygram-project
Anygram-project

![Workflow status](https://github.com/ouriso/foodgram-project/actions/workflows/anygram-workflow.yaml/badge.svg)

Развернутый проект можно [посмотреть по этой ссылке](http://thehedgehognotes.ml)

### Описание проекта
Проект предназначен для фотографов, которые могут выложить свои фотографию и  
поделиться "рецептом" ее создания:
- какие ингредиенты (реквизит) необходимо раздобыть, чтобы включить их в кадр
- время, которое нужно потратить для получения подобной фотографии
- последовательность действий при подготовке к съемке, рекомендации и полезные советы

Авторизованный пользователь может подписываться на авторов понравившихся им работ или  
добавлять интересные ему фото (рецепты) в список Избранного.  
Также любой пользователь может добавлять "рецепты" в корзину, где производится  
автоматический подсчет необходимых для съемок реквизитов (ингредиентов).  
Для получения всего списка в формате PDF можно нажать кнопку "Скачать список" на  
странице Списка покупок.

### Установка
#### Локальная установка и запуск
Для локального запуска проекта необходимо:
- установить и запустить виртуальное окружение, например:  
`python -m venv venv`

- установить указанные в файле requirements.txt зависимости командой:  
`pip install -r requirements.txt`

- создать в папке проекта `/src` файл `.env`, в котором указать значения необходимых  
переменных:  
`SECRET_KEY, DEBUG, DB_ENGINE, DB_NAME,  
POSTGRES_USER, POSTGRES_PASSWORD,  
DB_HOST, DB_PORT`

- установить и запустить базу данных
- выполнить миграции командой:  
`python manage.py migrate`

- локальный запуск осуществляется стандартной командой:  
`python manage.py runserver`

#### Запуск и установка в контейнерах Docker
Создание контейнера с проектом можно выполнить при помощи docker-файла  
`Dockerfile`, расположенного в корне проекта.

Для запуска проекта совместно с postgresql и nginx необходимо запустить  
docker-compose.yaml файл и выполнить миграции и сбор статики:  
`docker-compose up -d --force-recreate --build`  
`docker-compose exec -T web python3 manage.py collectstatic --no-input`  
`docker-compose exec -T web python3 manage.py migrate --noinput`

При этом также необходимо, чтобы были установлены переменные окружения  
или в папке с файлом docker-compose.yaml имелся файл .env с прописанными  
в нем переменными.

Настройки nginx для проекта раполагаются в файле `nginx/default.conf`.  
Для изменения настроек необходимо внести изменения в данный файл и  
перезапустить сборку контейнеров.
