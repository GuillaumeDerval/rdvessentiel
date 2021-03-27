from flask import Flask
app = Flask(__name__)

@app.route('/')
def count():
    return {'c': 0}
