from pathlib import Path
from services import database, config
import os
import hashlib
from datetime import datetime

config = config.get_config()

def index_dir(target_dir: Path, rebuild: bool = False, endswith: str = '.md'):
    target_dir = target_dir.expanduser()
    if not target_dir.is_dir():
        raise FileNotFoundError(target_dir)

    db = database.get_db()

    if rebuild:
        database.init_db()

    ignore_dirs = config.get('indexer', 'ignore_relative_dirs')

    # TODO: Change to use a less wasteful function
    for root, dirs, files in os.walk(target_dir):

        relative_dir = Path(root).relative_to(target_dir)

        ignore = False

        for dir in ignore_dirs:
            # print(f'relative_dir: [{str(relative_dir)}] | dir: {str(dir)} | {relative_dir.is_relative_to(Path(dir))}')
            if relative_dir.is_relative_to(Path(dir)):
                ignore = True

        if ignore:
            continue

        for file in files:
            if not file.endswith(endswith):
                continue

            file_path = Path(root) / file
            full_path = str(file_path)

            # title
            if file.endswith('.md'):
                title = file[:-3]
            else:
                title = file

            # TODO: handle rebuild logic

            # relative_file_path
            relative_file_path = file_path.relative_to(target_dir)

            # namespace
            namespace = 'me'

            # status
            status = 'draft'

            # visibility
            visibility = 'private'

            # file_hash
            with open(full_path, 'rb') as f:
                digest = hashlib.file_digest(f, 'sha256')
            file_hash = digest.hexdigest()

            # created_at
            created_at_epoch = os.path.getctime(full_path)
            created_at = datetime.fromtimestamp(created_at_epoch).strftime('%Y-%m-%d %H:%M:%S')

            # modified_at
            modified_at_epoch = os.path.getmtime(full_path)
            modified_at = datetime.fromtimestamp(modified_at_epoch).strftime('%Y-%m-%d %H:%M:%S')

            # last_indexed_at
            last_indexed_at = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

            query = '''
                INSERT INTO notes (
                    title,
                    relative_file_path,
                    namespace,
                    status,
                    visibility,
                    file_hash,
                    created_at,
                    modified_at,
                    last_indexed_at
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            '''
            params = [
                title,
                str(relative_file_path),
                namespace,
                status,
                visibility,
                file_hash,
                created_at,
                modified_at,
                last_indexed_at
            ]

            db.execute(query, params)
            db.commit()
