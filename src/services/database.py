import duckdb
from pathlib import Path
from services import config

config = config.get_config()

def init_db():
    db_path = Path(config.get_path('db_path', not_exists_ok=True))
    schema_path = Path(config.get_path('schema_path'))

    db = duckdb.connect(db_path)
    query = schema_path.read_text()

    db.execute(query)
    db.close()

def get_db():
    db_path = Path(config.get_path('db_path', not_exists_ok=True))

    if not db_path.exists():
        init_db()

    try:
        db = duckdb.connect(db_path)
    except IOError:
        raise IOError(f'Failed to get lock on {str(db_path)}')
    return db
