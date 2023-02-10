import json
import requests
import os
import psycopg2
from dotenv import load_dotenv

def get_weather(town):
    weather_url = f'https://api.weatherapi.com/v1/current.json?key=88936df545c5462c9ad134719230802&q={town}'
    response = requests.get(weather_url)
    weather_info = response.json()
    try:
        temp = weather_info['current']['temp_c']
        precip = weather_info['current']['precip_mm']
        create()
        return insert_data(town,temp,precip)
    except:
        return "error"

CREATE_TEST_TABLE = "CREATE TABLE IF NOT EXISTS weather(id SERIAL PRIMARY KEY,town_name TEXT UNIQUE, temp TEXT, precip TEXT);"
INSERT_IN_TABLE = "INSERT INTO weather(town_name,temp,precip) VALUES (%s,%s,%s) ON CONFLICT DO NOTHING;"
SELET_FROM_TABLE_WHERE = "SELECT town_name,temp,precip FROM weather WHERE town_name = (%s);"
DROP_TABLE = "DROP TABLE IF EXISTS weather;"

load_dotenv()

database_uri = os.environ["DATABASE_URI"]
connection = psycopg2.connect(database_uri)

def create():
    with connection:
        with connection.cursor() as cursor:
            cursor.execute(CREATE_TEST_TABLE)

def insert_data(town_name,temp,precip):
    with connection:
            with connection.cursor() as cursor:
                cursor.execute(INSERT_IN_TABLE, (f"{town_name}", f"Temperature in celsius: {temp}", f"Precipitation amount in millimeters: {precip}",),)

def select_from_weather(town_name):
        with connection:
            with connection.cursor() as cursor:
                try:
                    cursor.execute(SELET_FROM_TABLE_WHERE, (town_name,),)
                    return " ".join(cursor.fetchone())
                except:
                    return 'table does not exist'

def drop_table():
        with connection:
            with connection.cursor() as cursor:
                cursor.execute(DROP_TABLE)
