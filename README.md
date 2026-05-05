Структура проекта:

```mlops/
├── .github/
│   └── workflows/
│       └── ci.yml <- lint, test, docker build
│
├── app/
│   ├── data/
│   │   └── movielens.py
│   ├── model/
│   │   └── item_based.py
│   ├── inference/
│   │   └── recommend.py
│   └── api/
│       ├── main.py  <-  FastAPI app
│       ├── routes.py <- /recommend
│       └── schemas.py
│
├── bot/
│   ├── app/
│   │   ├── handlers.py
│   │   └── keyboards.py
│   └── main.py
│
├── tests/
│   ├── conftest.py <- matrix, model,
│   ├── test_recommend.py <- top_n, cold-start
│   └── test_edge_cases.py <- граничные случаи
│
├── ml-100k/         
├── .dockerignore
├── .flake8
├── docker-compose.yml <- локальный запуск API + volume
├── Dockerfile
├── pytest.ini 
├── requirements.txt
└── requirements-dev.txt 
```


### Как работает CI

При каждом push и pull request запускается `.github/workflows/ci.yml`:

```
push / pull request
        ↓
   build-test job
        ├── Lint       flake8 app bot
        ├── Test       pytest tests/
        └── Docker     docker build
```

Merge в `main` заблокирован если CI не прошёл (branch protection rule).


### Установка

```bash
git clone https://github.com/dudberoll/mlops.git
cd mlops

python3 -m venv .venv
source .venv/bin/activate

pip install -r requirements-dev.txt
```

### Запуск

**API**

```bash
uvicorn app.api.main:app --host 0.0.0.0 --port 8000
```

Эндпоинты:

| Метод | URL | Описание |
|---|---|---|
| GET | `/health` | статус сервиса |
| GET | `/recommend?user_id=1&n=10` | топ-N рекомендаций |
| GET | `/docs` | интерактивная документация |


**Docker**

```bash
docker compose up
```

Данные монтируются через volume — в образ не входят. При запуске Docker берёт папку ./ml-100k с хоста и делает её видимой внутри контейнера по пути /app/ml-100k. 


## Тесты

```bash
pytest tests/ -v
```

| Файл | Что тестирует |
|---|---|
| `test_recommend.py` | recommend() не возвращает просмотренные фильмы, результаты отсортированы по убыванию, cold-start возвращает пустой список, соблюдается лимит n |
| `test_edge_cases.py` | нулевой знаменатель не вызывает ZeroDivisionError, новый пользователь не получает уже оценённые фильмы, пустые оценки возвращают пустой список |

## Датасет

[MovieLens 100k](https://grouplens.org/datasets/movielens/100k/)

## Переменные окружения

| Переменная | Описание | По умолчанию |
|---|---|---|
| `DATA_PATH` | путь к `u.data` | `ml-100k/u.data` |
| `ITEM_PATH` | путь к `u.item` | `ml-100k/u.item` |
