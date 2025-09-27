# Instagram Info API

This API allows you to extract information from various Instagram URL types.

## Installation

Make sure you have the required dependencies:

```bash
uv pip install -r requirements.txt

# or

uv sync
```

## Running the Server

```bash
uv run server.py
# or
uvicorn api:app --host 0.0.0.0 --port 8000 --reload
```
## Build docker image

```bash
docker build -t insta-api .
docker run -p 8000:8000 insta-api
```

The API will be available at `http://localhost:8000`

## API Endpoints

### GET `/api/instagram-info`

Extract information from Instagram URLs.

#### Query Parameters
- `url` (required): The Instagram URL to extract information from

#### Supported URL Types
- Posts: `https://www.instagram.com/p/shortcode/`
- Reels: `https://www.instagram.com/reel/shortcode/`
- Profiles: `https://www.instagram.com/username/`

#### Example Request
```
GET /api/instagram-info?url=https://www.instagram.com/p/Cxyz123/
```

#### Example Response
```json
{
  "type": "post",
  "id": 1234567890123456789,
  "shortcode": "Cxyz123",
  "caption": "Example post caption",
  "owner_username": "username",
  "like_count": 123,
  "comment_count": 5,
  "media_type": "GraphImage",
  "media_url": "https://...",
  "is_video": false,
  "date_utc": "2023-01-01T12:00:00+00:00",
  "location": null
}
```
