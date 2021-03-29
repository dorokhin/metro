from utils import get_or_create_metro_line, get_or_create_subway_station, get_or_create_city
from useragent import random_user_agent
from urllib.error import HTTPError
from contextlib import closing
from dotenv import load_dotenv
import urllib.request
import urllib.parse
import psycopg2
import json
import gzip
import os

load_dotenv()


def get_json(url, headers=None):
    req = urllib.request.Request(
        url,
        data=None,
        headers=headers if headers else {
                'User-Agent': random_user_agent(),
                'Accept': 'text/html,application/xml;q=0.9,*/*;q=0.8',
                'Accept-Encoding': 'gzip, deflate',
                'Accept-Language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7',
        }
    )
    with urllib.request.urlopen(req) as response:
        if response.getcode() != 200:
            raise HTTPError(url, response.getcode(), None, {}, None)
        return gzip.decompress(response.read()).decode('utf-8')


if __name__ == '__main__':
    API_URL = 'https://api.hh.ru/metro/'
    json_data = json.loads(get_json(API_URL))
    towns = ['Москва', 'Санкт-Петербург']
    total_towns = 0
    total_lines = 0
    total_stations = 0
    with closing(psycopg2.connect(
            dbname=os.environ['dbname'],
            user=os.environ['user'],
            password=os.environ['password'],
            host=os.environ['host']
    )) as conn:
        with conn.cursor() as cursor:
            conn.autocommit = True
            for city in json_data:
                if city['name'] in towns:
                    city_created, city_id = get_or_create_city(cursor, city['name'])
                    if city_created:
                        total_towns += 1
                    for line in city['lines']:
                        line_created, line_id = get_or_create_metro_line(cursor, line['name'], line['hex_color'])
                        if line_created:
                            total_lines += 1
                        for station in line['stations']:
                            created, _ = get_or_create_subway_station(cursor, station, city_id, line_id)
                            if created:
                                total_stations += 1

    print('Total cities added:', total_towns)
    print('Total metro lines added:', total_lines)
    print('Total metro stations added:', total_stations)
