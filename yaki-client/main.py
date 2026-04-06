#!/usr/bin/env python3
import httpx
import typer
from commands import notes, utils

app = typer.Typer()

@app.command()
def health_check():
    utils.health_check()

@app.command()
def list_notes(
    status: str = typer.Argument(None),
    visibility: str = typer.Argument(None),
    project_title: str = typer.Argument(None),
    tag: str = typer.Argument(None)
):
    notes.list(status, visibility, project_title, tag)

@app.command()
def add(
    file_name: str = typer.Argument('.'),
    project_title: str = typer.Argument('yaki'),
    status: str = typer.Argument('draft'),
    visibility: str = typer.Argument('private'),
    retention_period_days: int = typer.Argument(0)
):
    notes.add(file_name, project_title, status, visibility, retention_period_days)

@app.command()
def add_dir(dir_name: str = typer.Argument('.')):
    notes.add_dir(dir_name)

if __name__ == '__main__':
    app()
