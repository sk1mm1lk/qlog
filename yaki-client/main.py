#!/usr/bin/env python3
import httpx
import typer

app = typer.Typer()
BASE_URL = 'http://localhost:8000'

@app.command()
def health_check():
    check_server()

    print('Server is up')

def check_server():
    try:
        httpx.get(f'{BASE_URL}/health')
    except httpx.ConnectError:
        print('yaki server is not running.')
        raise SystemExit(1)

@app.command()
def list_notes(
    status: str = None,
    visibility: str = None,
    project_title: str = None,
    tag: str = None
):
    check_server()
    params = {}
    if status:
        params['status'] = status
    if project:
        params['project'] = project
    if tag:
        params['tag'] = tag

    res = httpx.get(f'{BASE_URL}/notes/', params=params)
    for note in res.json():
        print(f"[{note['id']}] {note['title']}")

if __name__ == '__main__':
    app()
