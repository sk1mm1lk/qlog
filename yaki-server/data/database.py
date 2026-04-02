import duckdb
from pathlib import Path

DB_PATH = 'data/yaki.db' # TODO: $HOME/.local/share/yaki/yaki.db
DB_CREATE_DDL_PATH = Path('data/schema.sql')

def init_db():
    db = duckdb.connect(DB_PATH)
    query = DB_CREATE_DDL_PATH.read_text()
    db.execute(query)
    db.close()

def get_db():
    return duckdb.connect(DB_PATH)
