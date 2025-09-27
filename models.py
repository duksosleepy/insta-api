import re

from attrs import define, field, validators

_INSTAGRAM_URL_PATTERNS = [
    re.compile(r'/(?:p|reel)/([A-Za-z0-9_-]+)/?', re.IGNORECASE),
    re.compile(r'instagram\.com/([A-Za-z0-9._]+)/?(?:\?.*)?$', re.IGNORECASE),
    re.compile(r'/explore/tags/([^/?]+)/?', re.IGNORECASE),
]

_HTTP_PATTERN = re.compile(r'^https://', re.IGNORECASE)


def is_valid_instagram_url(instance, attribute, value: str) -> None:
    """Custom validator for Instagram URLs with detailed error messages."""

    if not _HTTP_PATTERN.match(value):
        raise ValueError(f"'{value}' must start with https://")

    if 'instagram.com' not in value.lower():
        raise ValueError(f"'{value}' must be from instagram.com domain")

    if not any(pattern.search(value) for pattern in _INSTAGRAM_URL_PATTERNS):
        raise ValueError(
            f"'{value}' has unsupported Instagram URL format. "
            + 'Supported formats: posts (/p/), reels (/reel/), profiles, hashtags (/explore/tags/)'
        )


@define(slots=False)
class InstagramRequest:
    """Request model for Instagram URL validation with comprehensive validation."""

    url: str = field(
        validator=[
            validators.instance_of(str),
            is_valid_instagram_url,
        ]
    )


@define(slots=False)
class PostResponse:
    """Response model for Instagram post/reel information with validation."""

    type: str = field(validator=validators.in_(['post', 'reel']))
    id: int = field(validator=validators.instance_of(int))
    shortcode: str = field(
        validator=[
            validators.instance_of(str),
            validators.matches_re(r'^[A-Za-z0-9_-]+$'),
        ]
    )
    caption: str = field(validator=validators.instance_of(str))
    owner_username: str = field(validator=validators.instance_of(str))
    like_count: int = field(validator=validators.instance_of(int))
    comment_count: int = field(validator=validators.instance_of(int))
    media_type: str = field(
        validator=validators.in_(['image', 'video', 'carousel'])
    )
    media_url: str = field(validator=validators.instance_of(str))
    is_video: bool = field(validator=validators.instance_of(bool))
    date_utc: str = field(validator=validators.instance_of(str))


@define(slots=False)
class ProfileResponse:
    """Response model for Instagram profile information with validation."""

    type: str = field(validator=validators.in_(['profile']))
    username: str = field(validator=validators.instance_of(str))
    userid: int = field(validator=validators.instance_of(int))
    full_name: str = field(validator=validators.instance_of(str))
    biography: str = field(validator=validators.instance_of(str))
    followers: int = field(validator=validators.instance_of(int))
    followees: int = field(validator=validators.instance_of(int))
    mediacount: int = field(validator=validators.instance_of(int))
    is_private: bool = field(validator=validators.instance_of(bool))
    is_verified: bool = field(validator=validators.instance_of(bool))
    profile_pic_url: str = field(validator=validators.instance_of(str))
    external_url: str = field(validator=validators.instance_of(str))


@define(slots=False)
class ErrorResponse:
    """Response model for API errors with validation."""

    error: str = field(
        validator=[validators.instance_of(str), validators.min_len(1)]
    )


InstagramResponse = PostResponse | ProfileResponse | ErrorResponse
