import requests
from celery import Celery

from .parsing import extract_user_data
from ..redis.config import settings

app = Celery('tasks', broker=settings.url, backend=settings.url)


@app.task
def parse_url(url):
    print('Parse url')
    doc = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'}).text
    print('Extract data')
    user_data = extract_user_data(doc)

    return user_data
