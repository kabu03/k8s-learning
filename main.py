from fastapi import FastAPI
import psycopg
import os

app = FastAPI()

@app.get("/hello")
def hello():
    return {"message": "hello"}

def get_conn():
    host = os.getenv("DB_HOST", "postgres")
    port = int(os.getenv("DB_PORT", "5432"))
    db   = os.getenv("DB_NAME")
    user = os.getenv("DB_USER")
    pw   = os.getenv("DB_PASSWORD")
    return psycopg.connect(host=host, port=port, dbname=db, user=user, password=pw)

@app.get("/db-check")
def db_check():
    with get_conn() as conn:
        with conn.cursor() as cur:
            cur.execute("CREATE TABLE IF NOT EXISTS demo (id SERIAL PRIMARY KEY, name TEXT);")
            cur.execute("INSERT INTO demo (name) VALUES (%s) RETURNING id;", ("hello-from-fastapi",))
            new_id = cur.fetchone()[0]
            cur.execute("SELECT COUNT(*) FROM demo;")
            count = cur.fetchone()[0]
    return {"inserted_id": new_id, "rows_in_table": count}