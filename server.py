import uvicorn

from shared.logging import init_logging

if __name__ == '__main__':
    init_logging()

    uvicorn.run(
        'api:app', host='127.0.0.1', port=8000, reload=True, log_config=None
    )
