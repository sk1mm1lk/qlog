import typer
from pathlib import Path
from services import indexer
from services import config

app = typer.Typer()
config = config.get_config()

'''
    status: str = typer.Argument(None),
    visibility: str = typer.Argument(None),
    project_title: str = typer.Argument(None),
    tag: str = typer.Argument(None)
'''

@app.command()
def index():
    # TODO: add these as optional arguments
    target_dir = config.get_dir('notes_dir') #Path('/home/m1lkie/documents/second-brain/')
    rebuild = True
    endswith = '.md'

    indexer.index_dir(target_dir, rebuild, endswith)

if __name__ == '__main__':
    app()
