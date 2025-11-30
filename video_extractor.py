"""
Video extraction from Instagram and X (Twitter) posts
"""

import logging
import asyncio
import os
from pathlib import Path
import yt_dlp

logger = logging.getLogger(__name__)

class VideoExtractor:
    """Extract videos from Instagram and X posts"""
    
    def __init__(self):
        self.download_dir = "videos"
        # Create videos directory if it doesn't exist
        Path(self.download_dir).mkdir(exist_ok=True)
    
    async def extract_video(self, url: str) -> dict:
        """
        Extract video from Instagram or X post
        Returns: {'success': bool, 'video_path': str, 'error': str}
        """
        try:
            if not self._is_valid_social_url(url):
                return {
                    'success': False,
                    'error': '❌ Please provide a valid Instagram or X (Twitter) post link'
                }
            
            # Run yt-dlp in executor to avoid blocking
            loop = asyncio.get_event_loop()
            result = await loop.run_in_executor(
                None,
                self._download_video,
                url
            )
            return result
            
        except Exception as e:
            logger.error(f"Error extracting video: {e}")
            return {
                'success': False,
                'error': f'❌ Error extracting video: {str(e)[:100]}'
            }
    
    def _is_valid_social_url(self, url: str) -> bool:
        """Check if URL is from Instagram or X"""
        url_lower = url.lower()
        return any(domain in url_lower for domain in [
            'instagram.com', 'instagr.am', 'insta.am',  # Instagram
            'x.com', 'twitter.com', 'post.x.com'  # X/Twitter
        ])
    
    def _download_video(self, url: str) -> dict:
        """Download video using yt-dlp"""
        try:
            ydl_opts = {
                'format': 'best[ext=mp4]/best',
                'outtmpl': os.path.join(self.download_dir, '%(id)s.%(ext)s'),
                'quiet': True,
                'no_warnings': True,
                'socket_timeout': 30,
            }
            
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(url, download=True)
                video_path = ydl.prepare_filename(info)
                
                if os.path.exists(video_path):
                    file_size = os.path.getsize(video_path) / (1024 * 1024)  # MB
                    
                    if file_size > 50:  # Telegram limit
                        os.remove(video_path)
                        return {
                            'success': False,
                            'error': f'❌ Video too large ({file_size:.1f}MB). Telegram limit is 50MB'
                        }
                    
                    return {
                        'success': True,
                        'video_path': video_path,
                        'title': info.get('title', 'Video')
                    }
                else:
                    return {
                        'success': False,
                        'error': '❌ Failed to download video'
                    }
                    
        except Exception as e:
            logger.error(f"yt-dlp error: {e}")
            error_msg = str(e).lower()
            
            if 'private' in error_msg or 'protected' in error_msg:
                return {'success': False, 'error': '❌ This video is private or protected'}
            elif 'age restricted' in error_msg:
                return {'success': False, 'error': '❌ This video is age-restricted'}
            elif 'unavailable' in error_msg:
                return {'success': False, 'error': '❌ This video is unavailable or deleted'}
            else:
                return {'success': False, 'error': f'❌ Download failed: {error_msg[:80]}'}
