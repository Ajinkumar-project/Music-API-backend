from ytmusicapi import YTMusic
from yt_dlp import YoutubeDL
import logging

logger = logging.getLogger(__name__)

ytmusic = YTMusic()


def get_home():
    return ytmusic.get_home()


def get_playlist(playlist_id):
    return ytmusic.get_playlist(playlist_id)


def get_album(album_id):
    return ytmusic.get_album(album_id)


def get_artist(artist_id):
    return ytmusic.get_artist(artist_id)


def get_charts():
    return ytmusic.get_charts()


def get_mood_categories():
    return ytmusic.get_mood_categories()


def search(query, filter_songs=False, limit=20):
    results = ytmusic.search(query, filter="songs" if filter_songs else None, limit=limit)
    return results


def get_song_stream_url(video_id):
    url = f"https://www.youtube.com/watch?v={video_id}"
    ydl_opts = {
        "format": "bestaudio/best",
        "quiet": True,
        "no_warnings": True,
        "extract_flat": False,
    }
    with YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=False)
        return {
            "url": info.get("url"),
            "title": info.get("title"),
            "duration": info.get("duration"),
            "thumbnail": info.get("thumbnail"),
            "ext": info.get("ext"),
        }
