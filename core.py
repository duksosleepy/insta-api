import re

import instaloader
from instaloader import Post, Profile
from loguru import logger

type dict_value = str | int | bool | None


class InstagramLoader:
    def __init__(self):
        self.L: instaloader.Instaloader = instaloader.Instaloader()
        logger.info('InstagramLoader initialized')

    def extract_from_url(self, url: str) -> dict[str, dict_value]:
        """Extract information from various Instagram URL types"""
        logger.info(f'Extracting info from URL: {url}')

        # Post URLs (/p/ or /reel/)
        post_match = re.search(r'/(?:p|reel)/([A-Za-z0-9_-]+)/', url)
        if post_match:
            result = self._extract_post_info(post_match.group(1))
            logger.info(
                f'Successfully extracted post info: {result["shortcode"]}'
            )
            return result

        # Profile URLs
        profile_match = re.search(r'instagram\.com/([A-Za-z0-9._]+)/?$', url)
        if profile_match:
            result = self._extract_profile_info(profile_match.group(1))
            logger.info(
                f'Successfully extracted profile info: {result["username"]}'
            )
            return result

        error_msg = f'Unsupported Instagram URL format: {url}'
        logger.warning(error_msg)
        return {'error': error_msg}

    def _extract_post_info(self, shortcode: str) -> dict[str, dict_value]:
        """Extract post/reel information and return PostResponse-ready data"""
        logger.debug(f'Extracting post info for shortcode: {shortcode}')
        try:
            post = Post.from_shortcode(self.L.context, shortcode)

            typename = 'GraphVideo' if post.is_video else 'GraphImage'
            if hasattr(post, 'sidecar_nodes') and post.sidecar_nodes:
                typename = 'GraphSidecar'
            product_type = (
                'clips'
                if (
                    post.is_video
                    and hasattr(post, 'video_duration')
                    and post.video_duration
                    and post.video_duration < 90
                )
                else ''
            )
            if typename == 'GraphVideo' and product_type == 'clips':
                content_type = 'reel'
                media_type = 'video'
            elif typename == 'GraphVideo':
                content_type = 'post'
                media_type = 'video'
            elif typename == 'GraphImage':
                content_type = 'post'
                media_type = 'image'
            elif typename == 'GraphSidecar':
                content_type = 'post'
                media_type = 'carousel'
            else:
                content_type = 'post'
                media_type = 'unknown'
            media_url = post.video_url if post.is_video else post.url
            result = {
                'type': content_type,
                'id': int(post.mediaid),
                'shortcode': post.shortcode,
                'caption': post.caption,
                'owner_username': post.owner_username,
                'like_count': post.likes,
                'comment_count': post.comments,
                'media_type': media_type,
                'media_url': media_url,
                'is_video': post.is_video,
                'date_utc': str(int(post.date_utc.timestamp()))
                if post.date_utc
                else '',
            }
            logger.success(
                f'Successfully extracted post info for shortcode: {shortcode}'
            )
            return result
        except Exception as e:
            error_msg = (
                f'Failed to extract post info for shortcode {shortcode}: {e}'
            )
            logger.error(error_msg)
            return {'error': error_msg}

    def _extract_profile_info(self, username: str) -> dict[str, dict_value]:
        """Extract profile information and return ProfileResponse-ready data"""
        logger.debug(f'Extracting profile info for username: {username}')
        try:
            profile = Profile.from_username(self.L.context, username)
            result = {
                'type': 'profile',
                'username': profile.username,
                'userid': int(profile.userid),
                'full_name': profile.full_name,
                'biography': profile.biography,
                'followers': profile.followers,
                'followees': profile.followees,
                'mediacount': profile.mediacount,
                'is_private': profile.is_private,
                'is_verified': profile.is_verified,
                'profile_pic_url': profile.profile_pic_url,
                'external_url': profile.external_url,
            }
            logger.success(
                f'Successfully extracted profile info for username: {username}'
            )
            return result
        except Exception as e:
            error_msg = (
                f'Failed to extract profile info for username {username}: {e}'
            )
            logger.error(error_msg)
            return {'error': error_msg}
