import httpx
from pathlib import Path
import os
import time
import errno
from commands import utils, projects
from config.server import BASE_URL
from datetime import datetime, timezone
import hashlib
import base64

# C

## add (existing note file (.md etc.))

# def add(add_name: str = '.'):
#     utils.check_server()
#     add_path = Path(add_name)
#
#     if add_path.is_dir():
#         add_dir(add_path)
#     elif not add_path.exists():
#         raise FileNotFoundError(errno.ENOENT, os.strerror(errno.ENOENT), add_name)
#
#     print(add_path)
#
# def add_dir(dir_name: str = '.'):
#     utils.check_server()
#     dir_path = Path(dir_name)
#
#     if dir_path.is_dir():
#         for root, _, files in os.walk(dir_path):
#             for file in files:
#                 file_path = Path(root, file)
#                 if file_path.name.endswith('.md'):
#                     print(file_path)
#     else:
#         raise NotADirectoryError(errno.ENOENT, os.strerror(errno.ENOENT), dir_name)

def add(
    file_name: str = '',
    project_title: str = 'yaki',
    status: str = "draft",
    visibility: str = "private",
    retention_period_days: int = 0
):
    utils.check_server()
    file_path = Path(file_name)

    if not file_path.exists():
        raise FileNotFoundError(errno.ENOENT, os.strerror(errno.ENOENT), file_name)

    # title
    title_list = file_name.split('.')[:-1] # get all before last . extension # TODO: this assumes .md and not compressed .md.gz
    title = '.'.join(title_list)

    # relative_file_path
    relative_file_path = projects.get_relative_file_path(project_title, file_path.resolve())

    # contents
    with open(file_path, 'rb') as file:
        contents_bytes = file.read()
    contents = base64.b64encode(contents_bytes).decode('ascii')

    # last_confirmed_at
    last_confirmed_at = datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M:%S')

    # file_hash
    #file_hash, hash_algorithm = utils.file_hash(contents)
    # TODO: move to utils
    m = hashlib.sha256()
    m.update(contents_bytes)
    file_hash_bytes = m.digest()
    file_hash = base64.b64encode(file_hash_bytes).decode('ascii')
    hash_algorithm = 'sha256'

    # created_at
    created_at_epoch = os.path.getctime(file_path)
    created_at = datetime.fromtimestamp(created_at_epoch, timezone.utc).strftime('%Y-%m-%d %H:%M:%S')

    # modified_at
    modified_at_epoch = os.path.getmtime(file_path)
    modified_at = datetime.fromtimestamp(modified_at_epoch, timezone.utc).strftime('%Y-%m-%d %H:%M:%S')

    data = {
        'title' : title,
        'project_title' : project_title,
        'relative_file_path' : relative_file_path,
        'status' : status,
        'visibility' : visibility,
        'retention_period_days' : retention_period_days,
        'contents' : contents, # TODO: could be the issue
        'last_confirmed_at' : last_confirmed_at,
        'file_hash' : file_hash,
        'hash_algorithm' : hash_algorithm,
        'created_at' : created_at,
        'modified_at' : modified_at
    }

    for key, value in data.items():
        print(f'{key}: {type(value)}')

    res = httpx.post(f'{BASE_URL}/notes/', json=data)
    res.raise_for_status()

## create (new note to a file (any file kind))
## ingest (existing note files recursively in a directory (flag passed for matching patterns))

# R

## list (list all notes (where possibly included)

def list(
    status: str = None,
    visibility: str = None,
    project_title: str = None,
    tag: str = None
):
    utils.check_server()
    params = {}
    if status:
        params['status'] = status
    if project_title:
        params['project_title'] = project_title
    if tag:
        params['tag'] = tag

    res = httpx.get(f'{BASE_URL}/notes/', params=params)
    for note in res.json():
        print(f"[{note['id']}] {note['title']}")

## list-project (list all notes in current project)
## read (read a detailed note response)

# U

## update (update existing note)
## index (update existing notes recursively in a directory, add if not exists (flag passed, default don't add))

# D

## delete (delete existing note)
## drop (delete existing notes recursively in a directory)
