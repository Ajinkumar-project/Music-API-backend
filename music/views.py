from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .services import (
    get_home,
    get_playlist,
    get_album,
    get_artist,
    get_charts,
    get_mood_categories,
    search,
    get_song_stream_url,
)
from .serializers import (
    PlaylistSerializer,
    AlbumSerializer,
    ArtistSerializer,
    HomeItemSerializer,
    SearchResultSerializer,
    StreamUrlSerializer,
)
from ytmusicapi import YTMusic
import logging

logger = logging.getLogger(__name__)

ytmusic = YTMusic()


class HomeAPIView(APIView):
    def get(self, request):
        logger.info("HomeAPIView called: path=%s method=%s", request.path, request.method)
        try:
            data = get_home()
            return Response({"results": data}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class PlaylistAPIView(APIView):
    def get(self, request, playlist_id):
        logger.info("PlaylistAPIView called: path=%s method=%s playlist_id=%s", request.path, request.method, playlist_id)
        try:
            data = get_playlist(playlist_id)
            serializer = PlaylistSerializer(data)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class AlbumAPIView(APIView):
    def get(self, request, album_id):
        logger.info("AlbumAPIView called: path=%s method=%s album_id=%s", request.path, request.method, album_id)
        try:
            data = get_album(album_id)
            serializer = AlbumSerializer(data)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class ArtistAPIView(APIView):
    def get(self, request, artist_id):
        logger.info("ArtistAPIView called: path=%s method=%s artist_id=%s", request.path, request.method, artist_id)
        try:
            data = get_artist(artist_id)
            serializer = ArtistSerializer(data)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class GenreAPIView(APIView):
    def get(self, request, genre_name=None):
        logger.info("GenreAPIView called: path=%s method=%s genre_name=%s", request.path, request.method, genre_name)
        try:
            if genre_name:
                categories = get_mood_categories()
                genre_params = None
                for category in categories.values():
                    for genre in category:
                        if genre["title"].lower() == genre_name.lower():
                            genre_params = genre["params"]
                            break
                    if genre_params:
                        break
                if genre_params:
                    try:
                        playlists = ytmusic.get_mood_playlists(genre_params)
                    except Exception:
                        playlists = search(f"{genre_name} playlist", filter_songs=False)
                    return Response({"results": playlists}, status=status.HTTP_200_OK)
                return Response({"error": f"Genre '{genre_name}' not found"}, status=status.HTTP_404_NOT_FOUND)
            data = get_mood_categories()
            return Response({"results": data}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class PopAPIView(APIView):
    def get(self, request):
        logger.info("PopAPIView called: path=%s method=%s", request.path, request.method)
        try:
            data = get_charts()
            return Response({"results": data}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class SearchAPIView(APIView):
    def get(self, request):
        logger.info("SearchAPIView called: path=%s method=%s query=%s", request.path, request.method, request.query_params.get("q", ""))
        query = request.query_params.get("q", "")
        if not query:
            return Response({"error": "Query parameter 'q' is required"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            results = search(query, filter_songs=True)
            serializer = SearchResultSerializer(results, many=True)
            return Response({"results": serializer.data}, status=status.HTTP_200_OK)
        except Exception as e:
            logger.error("SearchAPIView error: %s", str(e))
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class StreamURLAPIView(APIView):
    def get(self, request, video_id):
        logger.info("StreamURLAPIView called: path=%s method=%s video_id=%s", request.path, request.method, video_id)
        try:
            data = get_song_stream_url(video_id)
            serializer = StreamUrlSerializer(data)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except ValueError as e:
            logger.error("StreamURLAPIView validation error: %s", str(e))
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            logger.error("StreamURLAPIView error: %s", str(e))
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
