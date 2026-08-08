from rest_framework import serializers


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

