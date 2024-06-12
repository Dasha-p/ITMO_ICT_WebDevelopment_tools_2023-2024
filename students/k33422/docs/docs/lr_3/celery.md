# Документация Celery

В предоставленном коде используется Celery для асинхронной обработки задач парсинга веб-страниц.

## Настройка Celery

```python
from celery import Celery
from ..redis.config import settings

app = Celery('tasks', broker=settings.url, backend=settings.url)
```

Здесь создается экземпляр приложения Celery с именем `'tasks'`. Параметры `broker` и `backend` устанавливаются в URL Redis,
который берется из настроек `settings.url`. Брокер используется для отправки задач в очередь, а бэкенд - для хранения
результатов задач.

## Определение задачи Celery

```python
@app.task
def parse_url(url):
    print('Parse url')
    doc = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'}).text
    print('Extract data')
    user_data = extract_user_data(doc)

    return user_data
```

Декоратор `@app.task` используется для определения функции `parse_url` как задачи Celery. Эта функция принимает URL в качестве
аргумента и выполняет следующие шаги:

1. Отправляет GET-запрос к указанному URL с помощью библиотеки `requests`, передавая заголовок `User-Agent` для имитации
   запроса от браузера.
2. Извлекает HTML-содержимое страницы из ответа запроса.
3. Вызывает функцию `extract_user_data` для извлечения данных пользователя из HTML-содержимого.
4. Возвращает извлеченные данные пользователя в качестве результата задачи.

## Создание задачи Celery

```python
@router.post('/parsing', response_model=Annotated[TaskResponse, Depends()])
def create_task(data: Annotated[TaskRequest, Body()]):
    print('Try')
    task = parse_url.delay(data.url)
    print('task send')
    return TaskResponse(id=task.id)
```

Этот код определяет маршрут FastAPI для создания новой задачи парсинга. Когда клиент отправляет POST-запрос на `/parsing` с URL
в теле запроса, выполняются следующие действия:

1. Вызывается метод `parse_url.delay(data.url)`, который создает новую задачу Celery для парсинга указанного URL. Метод `delay`
   отправляет задачу в очередь для асинхронного выполнения.
2. Задача возвращает объект `AsyncResult`, который содержит информацию о задаче, такую как идентификатор задачи (`task.id`).
3. Функция возвращает объект `TaskResponse` с идентификатором созданной задачи.

## Получение результатов задачи Celery

```python
@router.get('/parsing/{task_id}', response_model=Annotated[TaskResponse, Depends()])
def get_task(task_id: str):
    task = parse_url.AsyncResult(task_id)
    return TaskResponse(id=task.id, status=task.status, data=task.result)
```

Этот код определяет маршрут FastAPI для получения результатов задачи парсинга по ее идентификатору. Когда клиент отправляет
GET-запрос на `/parsing/{task_id}`, выполняются следующие действия:

1. Вызывается метод `parse_url.AsyncResult(task_id)`, который создает объект `AsyncResult` для задачи с указанным
   идентификатором.
2. Объект `AsyncResult` содержит информацию о задаче, такую как идентификатор задачи (`task.id`), статус задачи (`task.status`)
   и результат задачи (`task.result`).
3. Функция возвращает объект `TaskResponse` с идентификатором задачи, статусом и результатом (если задача завершена).

---