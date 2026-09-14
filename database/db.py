import sqlite3
import os
from flask import g, has_app_context
from config import Config

def get_db():
    if has_app_context():
        if 'db' not in g:
            g.db = sqlite3.connect(
                Config.DATABASE,
                detect_types=sqlite3.PARSE_DECLTYPES
            )
            g.db.row_factory = sqlite3.Row
            g.db.execute("PRAGMA foreign_keys = ON;")
        return g.db
    else:
        db = sqlite3.connect(Config.DATABASE, detect_types=sqlite3.PARSE_DECLTYPES)
        db.row_factory = sqlite3.Row
        db.execute("PRAGMA foreign_keys = ON;")
        return db

def close_db(e=None):
    if has_app_context():
        db = g.pop('db', None)
        if db is not None:
            db.close()

def init_db(app=None):
    db_dir = os.path.dirname(Config.DATABASE)
    if not os.path.exists(db_dir):
        os.makedirs(db_dir, exist_ok=True)
        
    db = sqlite3.connect(Config.DATABASE)
    db.execute("PRAGMA foreign_keys = ON;")
    with open(Config.SCHEMA, 'r', encoding='utf-8') as f:
        db.executescript(f.read())
    db.commit()
    db.close()

def query_db(query, args=(), one=False):
    db = get_db()
    cur = db.execute(query, args)
    rv = cur.fetchall()
    cur.close()
    if not has_app_context():
        db.close()
    return (rv[0] if rv else None) if one else rv

def execute_db(query, args=()):
    db = get_db()
    cur = db.execute(query, args)
    db.commit()
    last_id = cur.lastrowid
    cur.close()
    if not has_app_context():
        db.close()
    return last_id
