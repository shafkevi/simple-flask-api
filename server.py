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
    user=os.getenv('username')
    password=os.getenv('password')
    conn = psycopg2.connect(dbname=dbname,
                            user=user,
                            host=host,
                            port=port,
                            password=password
                           )
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