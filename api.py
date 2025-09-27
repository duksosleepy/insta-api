import urllib.parse

from cattrs.preconf.orjson import make_converter
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from loguru import logger

from core import InstagramLoader
from models import (
    ErrorResponse,
    InstagramRequest,
    PostResponse,
    ProfileResponse,
)
from shared.logging import init_logging

init_logging()

app = FastAPI(
    title='Instagram Info API',
    description='API to get information from Instagram URLs',
)


app.add_middleware(
    CORSMiddleware,
    allow_origins=['127.0.0.1:3000'],
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*'],
)

converter = make_converter()


@app.exception_handler(HTTPException)
async def http_exception_handler(request: InstagramRequest, exc: HTTPException):
    """Convert HTTPException to ErrorResponse format."""
    logger.error(f'HTTPException occurred: {exc.status_code} - {exc.detail}')

    error_response = converter.structure(
        {'error': exc.detail},
        ErrorResponse,
    )
    return JSONResponse(
        status_code=exc.status_code,
        content=converter.unstructure(error_response),
    )


@app.get('/api/instagram-info')
async def get_instagram_info(
    url: str,
):
    """
    Supported URL types:
    - Posts: https://www.instagram.com/p/shortcode/
    - Reels: https://www.instagram.com/reel/shortcode/
    - Profiles: https://www.instagram.com/username/
    """
    try:
        url_request = InstagramRequest(url=url)
        validated_url = url_request.url
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

    decoded_url = urllib.parse.unquote(validated_url)

    extractor = InstagramLoader()

    try:
        result = extractor.extract_from_url(decoded_url)

        match result:
            case {'type': 'post', **rest} | {'type': 'reel', **rest}:
                return converter.structure(result, PostResponse)
            case {'type': 'profile', **rest}:
                return converter.structure(result, ProfileResponse)
            case _:
                raise HTTPException(
                    status_code=400,
                    detail='Cannot reach url, please check again.',
                )
    except HTTPException:
        raise


@app.get('/ping')
async def ping():
    return {'message': 'pong'}


@app.get('/')
async def root():
    return {
        'message': 'Instagram Info API',
        'endpoints': {
            '/api/instagram-info': {
                'methods': ['GET'],
                'GET': {
                    'params': {
                        'url': 'Instagram URL to extract info from (required)',
                    },
                    'example': '/api/instagram-info?url=https://www.instagram.com/p/...',
                },
            }
        },
        'documentation': {'swagger': '/docs', 'redoc': '/redoc'},
    }
