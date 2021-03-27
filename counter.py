from flask import Flask
import os
import psycopg2
from flask_cors import CORS

DATABASE_URL = os.environ['DATABASE_URL']

app = Flask(__name__)
CORS(app)

@app.route('/')
def count():
    conn = psycopg2.connect(DATABASE_URL, sslmode='require')
    cur = conn.cursor()
    cur.execute("UPDATE count SET c=c+1")
    conn.commit()
    cur.close()
    cur = conn.cursor()
    cur.execute("SELECT c FROM count")
    c = cur.fetchone()
    cur.close()
    return {'c': c}
