from django.urls import path
from .views import (
    HomeAPIView,
    PlaylistAPIView,
    AlbumAPIView,
    ArtistAPIView,
    GenreAPIView,
    PopAPIView,
    SearchAPIView,
    StreamURLAPIView,
)
from .auth_views import LoginView, RefreshTokenView, LogoutView, RegisterView

urlpatterns = [
    path("auth/login/", LoginView.as_view(), name="login"),
    path("auth/refresh/", RefreshTokenView.as_view(), name="refresh"),
    path("auth/logout/", LogoutView.as_view(), name="logout"),
    path("auth/register/", RegisterView.as_view(), name="register"),
    path("home/", HomeAPIView.as_view(), name="home"),
    path("playlist/<str:playlist_id>/", PlaylistAPIView.as_view(), name="playlist"),
    path("album/<str:album_id>/", AlbumAPIView.as_view(), name="album"),
    path("artist/<str:artist_id>/", ArtistAPIView.as_view(), name="artist"),
    path("genre/", GenreAPIView.as_view(), name="genre-list"),
    path("genre/<str:genre_name>/", GenreAPIView.as_view(), name="genre"),
    path("pop/", PopAPIView.as_view(), name="pop"),
    path("search/", SearchAPIView.as_view(), name="search"),
    path("stream/<str:video_id>/", StreamURLAPIView.as_view(), name="stream"),
]
