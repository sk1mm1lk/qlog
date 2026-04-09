import typer
from pathlib import Path
from services import parser
from services import config

app = typer.Typer()
config = config.get_config()

@app.command()
def parse():
    target_dir = config.get_dir('notes_dir')
    rebuild = True
    parse_tags = True
    parse_links = True

    parser.parse_dir(target_dir, rebuild, parse_tags, parse_links)

if __name__ == '__main__':
    app()
