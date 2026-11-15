import sqlite3
import json
from pathlib import Path
DB_PATH = Path(__file__).with_name("simulations.db")

def connect():
    con = sqlite3.connect(DB_PATH)
    con.row_factory = sqlite3.Row
    return con

def initialize_db():
    with connect() as con:
        con.execute("""CREATE TABLE IF NOT EXISTS simulations (
            id INTEGER PRIMARY KEY AUTOINCREMENT, created_at TEXT DEFAULT CURRENT_TIMESTAMP,
            dataset TEXT, policy TEXT, config TEXT, metrics TEXT, rows_json TEXT
        )""")

def save_run(dataset, result):
    initialize_db()
    with connect() as con:
        cur = con.execute("INSERT INTO simulations(dataset, policy, config, metrics, rows_json) VALUES(?,?,?,?,?)",
            (dataset, result["policy"], json.dumps(result["config"]), json.dumps(result["metrics"]),
             json.dumps(result["rows"])))
        return cur.lastrowid

def list_runs():
    initialize_db()
    with connect() as con:
        return [dict(r) for r in con.execute("SELECT id, created_at, dataset, policy, config, metrics FROM simulations ORDER BY id DESC")]

def get_run(run_id):
    with connect() as con:
        row = con.execute("SELECT * FROM simulations WHERE id=?", (int(run_id),)).fetchone()
        return dict(row) if row else None

def count_runs():
    initialize_db()
    with connect() as con:
        return con.execute("SELECT COUNT(*) FROM simulations").fetchone()[0]
