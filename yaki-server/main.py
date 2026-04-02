from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routers import notes
from data.database import init_db

app = FastAPI(
    title='yaki API',
    description='A Markdown native wiki API',
    version='0.1.0'
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=['http://localhost:5173'],  # For future use for Svelte
    allow_methods=['*'],
    allow_headers=['*']
)

app.include_router(notes.router)

@app.on_event('startup')
def startup():
    init_db()

@app.get('/health')
def health():
    return {'status': 'ok'}

@app.get('/version')
def version():
    return {"api_version": "1"}
