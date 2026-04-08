import typer
from commands import index

app = typer.Typer()

app.add_typer(index.app)

if __name__ == '__main__':
    app()
