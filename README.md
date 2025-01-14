# FastAPI - грибы в корзинке

## Требования

* [Docker](https://www.docker.com/)
* python 3.10 - python 3.12 
* pydantic
* fastapi

## Запуск в Docker

```bash
$ cp ./docker-compose.override.yml{.dist,}
```

#### docker-compose.override.yml
При необходимости в этом файле можно изменить внешний порт с `8000` на любой другой.

Так же можно изменить команду на запуск в dev режиме на `fastapi run --reload app/main.py` вместо стандартной `fastapi run app/main.py`.

#### Сборка и запуск
```bash
$ docker compose up -d 
```


## Обычный запуск

Установка зависимостей (делается 1 раз)
```bash
$ python3 -m venv .venv 
$ .venv/bin/pip3 install -r ./requirements.txt
```

Активация окружения
```bash
$ source ./.venv/bin/activate
```

Запуск в `production` режиме (где workders = кол-во потоков)
```bash
$ fastapi run --workers 4 app/main.py
```

Запуск в `dev` режиме (автоматический перезапуск при изменениях)
```bash
$ fastapi run --reload app/main.py 
```

Запуск в `debug` режиме (в PyCharm)
```bash
$ python3 ./app/run_api_server.py
```

## Приложение

По-умолчанию приложение доступно по адресу http://localhost:8000. 
Если у вас открывается http://localhost:8000/api/utils/health-check значит все настроено верно 

## API документация

При запуске с помощью команды `fastapi` автоматически создается документация в формате openapi по ссылке
http://localhost:8000/docs