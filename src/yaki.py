import typer
from commands import index, parse

app = typer.Typer()

app.add_typer(index.app)
app.add_typer(parse.app)

if __name__ == '__main__':
    app()
