import uuid
from datetime import date

import psycopg2
from bs4 import BeautifulSoup

DB_HOST = 'postgres'
DB_PORT = '5432'
DB_NAME = 'travel'
DB_USER = 'postgres'
DB_PASSWORD = 'postgres'


def get_db_connection():
    return psycopg2.connect(
        dbname=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD,
        host=DB_HOST,
        port=DB_PORT
    )


def insert_user_data(user_data_list):
    conn = get_db_connection()
    cur = conn.cursor()
    query = '''
        INSERT INTO "user" (
        email,
        first_name,
        last_name,
        gender,
        birth_date,
        description,
        county,
        language,
        password_hash
        )
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
    '''

    cur.executemany(query, list(map(refill_data_to_db, user_data_list)))
    conn.commit()
    cur.close()
    conn.close()


def refill_data_to_db(user_data):
    return (
        user_data.get('email', 'test@test.test'),
        user_data.get('first_name', 'test_first_name'),
        user_data.get('last_name', 'test_last_name'),
        user_data.get('gender', 'male'),
        user_data.get('birth_date', '2024-01-01'),
        user_data.get('description', 'test_description'),
        user_data.get('county', 'Russia'),
        user_data.get('language', 'ru'),
        user_data.get('password_hash', b'test_hash')
    )


def extract_user_data(page):
    soup = BeautifulSoup(page, 'html.parser')

    results = []

    for i, card in enumerate(soup.select('div.card-n__body')):
        name, age = (
            card
            .select_one('p.card-n__title.card-n__title--find.companion')
            .get_text(strip=True)
            .split(', ')
        )
        city = (
            card
            .select_one('li.card-n__info-item.city')
            .get_text(strip=True)
            .replace('Откуда:', '').strip())

        results.append(
            {
                'email': f'{str(uuid.uuid4())[:8]}@mail.ru',
                'first_name': name,
                'birth_date': date(date.today().year - int(age), 1, 1).strftime('%Y-%m-%d'),
                'description': city
            }
        )

    return results
