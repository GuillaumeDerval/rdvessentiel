from flask import Flask
import os
import psycopg2

DATABASE_URL = os.environ['DATABASE_URL']
conn = psycopg2.connect(DATABASE_URL, sslmode='require')
app = Flask(__name__)

@app.route('/')
def count():
    cur = conn.cursor()
    cur.execute("UPDATE count SET c=c+1")
    conn.commit()
    cur.close()
    cur = conn.cursor()
    c = cur.execute("SELECT c FROM count").fetchone()
    cur.close()
    return {'c': c}
