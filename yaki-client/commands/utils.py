import httpx

BASE_URL = 'http://localhost:8000'

def health_check():
    check_server()

    print('Server is up')

def check_server():
    try:
        httpx.get(f'{BASE_URL}/health')
    except httpx.ConnectError:
        print('yaki server is not running.')
        raise SystemExit(1)

