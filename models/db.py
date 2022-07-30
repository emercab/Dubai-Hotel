import sqlite3
from flask import g

DATABASE = './models/database.db'

def conectar():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
    return db

@app.teardown_appcontext
def close(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()
