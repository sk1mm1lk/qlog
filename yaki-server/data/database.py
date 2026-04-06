import duckdb
from pathlib import Path
import socket

DB_PATH = 'data/yaki.db' # TODO: $HOME/.local/share/yaki/yaki.db
DB_CREATE_DDL_PATH = Path('data/schema.sql')

def init_db():
    db = duckdb.connect(DB_PATH)
    query = DB_CREATE_DDL_PATH.read_text()
    db.execute(query)

    system_name = socket.gethostname()

    query = """
        INSERT INTO projects (
            title,
            root_file_path,
            system
        ) VALUES (?, ?, ?);
    """
    params = ('yaki', '/', system_name)
    db.execute(query, params)

    db.close()

def get_db():
    return duckdb.connect(DB_PATH)
