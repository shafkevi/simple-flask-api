from fastapi import FastAPI
import psycopg2
from psycopg2.extras import RealDictCursor

import os

app = FastAPI()

try:
    print(os.environ)
    # Just good ol' env variables
    dbname=os.getenv('dbname')
    host=os.getenv('dbhost')
    port=os.getenv('dbport')
    # Coming from secrets manager
    user=os.getenv('dbuser')
    password=os.getenv('dbpass')
    conn = psycopg2.connect(dbname=dbname,
                            user=user,
                            host=host,
                            port=port,
                            password=password
                           )
    conn.set_session(autocommit=True)

except Exception as e:
    print("I am unable to connect to the database", e)


@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.get("/env")
async def env():
    print(os.environ)
    return {"message": "Hello env"}

@app.get("/tables")
async def tables():
    cursor = conn.cursor(cursor_factory=RealDictCursor)
    cursor.execute("select * from information_schema.tables;")
    tables = cursor.fetchall()
    cursor.close()
    return tables


@app.get("/pg/init")
async def pg_init():
    cursor = conn.cursor(cursor_factory=RealDictCursor)
    cursor.execute("create table if not exists items (key text primary key, value text)")
    cursor.close()


@app.get("/pg/destroy")
async def pg_destroy():
    cursor = conn.cursor(cursor_factory=RealDictCursor)
    cursor.execute("drop table items")
    cursor.close()



@app.get("/pg/put/{key}/{value}")
async def pg_put_key_value(key, value):
    cursor = conn.cursor(cursor_factory=RealDictCursor)
    cursor.execute("insert into items(key, value) VALUES('{key}','{value}') on conflict (key) do update set value = '{value}';".format(**{"key": key, "value": value}))
    cursor.close()


@app.get("/pg/get")
async def pg_get():
    cursor = conn.cursor(cursor_factory=RealDictCursor)
    cursor.execute("select * from items;")
    items = cursor.fetchall()
    cursor.close()
    return items

@app.get("/pg/get/{key}")
async def pg_get_key(key):
    cursor = conn.cursor(cursor_factory=RealDictCursor)
    cursor.execute("select * from items where key = '{key}';".format(**{"key": key}))
    items = cursor.fetchall()
    cursor.close()
    return items