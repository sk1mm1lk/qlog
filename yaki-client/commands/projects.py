import httpx
from pathlib import Path
import os
import errno
from config.server import BASE_URL

def get_relative_file_path(project_title: str, file_path: str):
    # TODO: This should return the relative path to the project
    # TODO: schema.yaml should set 'yaki' as root from the start
    return str(file_path)
