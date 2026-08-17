from rest_framework import serializers


from django.contrib.auth import get_user_model
from rest_framework import serializers

User = get_user_model()


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    password2 = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'password2']

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({"password": "Passwords do not match"})
        return attrs

    def create(self, validated_data):
        validated_data.pop('password2')
        return User.objects.create_user(**validated_data)


def pick_thumbnail(thumbnails, video_id=None):
    if video_id:
        return f"https://i.ytimg.com/vi/{video_id}/maxresdefault.jpg"
    if thumbnails and isinstance(thumbnails, list) and len(thumbnails) > 0:
        last = thumbnails[-1]
        if isinstance(last, dict) and last.get("url"):
            return last["url"]
    return None


def normalize_track(item):
    video_id = item.get("videoId") or item.get("video_id")
    return {
        "id": video_id,
        "title": item.get("title", ""),
        "video_id": video_id,
        "artists": item.get("artists", []),
        "album": item.get("album"),
        "duration": item.get("duration"),
        "thumbnail": pick_thumbnail(item.get("thumbnails"), video_id),
    }


class TrackSerializer(serializers.Serializer):
    id = serializers.CharField(required=False)
    title = serializers.CharField()
    video_id = serializers.CharField(required=False)
    artists = serializers.ListField(child=serializers.DictField(), required=False)
    album = serializers.CharField(required=False)
    duration = serializers.CharField(required=False)
    thumbnail = serializers.URLField(required=False)


class PlaylistSerializer(serializers.Serializer):
    id = serializers.CharField(required=False)
    title = serializers.CharField()
    description = serializers.CharField(required=False)
    thumbnail = serializers.URLField(required=False)
    tracks = TrackSerializer(many=True, required=False)
    track_count = serializers.IntegerField(required=False)


class AlbumSerializer(serializers.Serializer):
    id = serializers.CharField(required=False)
    title = serializers.CharField()
    year = serializers.CharField(required=False)
    thumbnail = serializers.URLField(required=False)
    tracks = TrackSerializer(many=True, required=False)
    artists = serializers.ListField(child=serializers.DictField(), required=False)


class ArtistSerializer(serializers.Serializer):
    channel_id = serializers.CharField(source="channelId")
    name = serializers.CharField()
    subscribers = serializers.CharField(required=False)
    thumbnails = serializers.ListField(child=serializers.DictField(), required=False)
    description = serializers.CharField(required=False)
    views = serializers.CharField(required=False)
    songs = serializers.DictField(required=False)
    albums = serializers.DictField(required=False)
    singles = serializers.DictField(required=False)
    videos = serializers.DictField(required=False)
    related = serializers.DictField(required=False)


class HomeItemSerializer(serializers.Serializer):
    title = serializers.CharField()
    contents = serializers.ListField(child=serializers.DictField())


class SearchResultSerializer(serializers.Serializer):
    title = serializers.CharField()
    resultType = serializers.CharField()
    videoId = serializers.CharField(required=False)
    browseId = serializers.CharField(required=False)
    category = serializers.CharField(required=False)
    artists = serializers.ListField(child=serializers.DictField(), required=False)
    album = serializers.DictField(required=False)
    thumbnail = serializers.URLField(required=False)


class StreamUrlSerializer(serializers.Serializer):
    url = serializers.URLField()
    title = serializers.CharField()
    duration = serializers.IntegerField()
    thumbnail = serializers.URLField()
    ext = serializers.CharField()

