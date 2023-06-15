from rest_framework import serializers
from . import models

class SongReviewCommentSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='user.username')
    user_id = serializers.ReadOnlyField(source='user.id')
    song_review = serializers.ReadOnlyField(source='song_review.id')

    class Meta:
        model = models.SongReviewComment
        fields = ['song_review', 'content', 'user', 'user_id'] 

class SongReviewSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='user.username')
    user_id = serializers.ReadOnlyField(source='user.id')
    comments = SongReviewCommentSerializer(many=True, read_only=True)
    comments_count = serializers.SerializerMethodField()
    likes_count = serializers.SerializerMethodField()
    song_picture = serializers.SerializerMethodField()

    def get_comments_count(self, obj):
        return models.SongReviewComment.objects.filter(song_review=obj).count()
    
    def get_likes_count(self, obj):
        return models.SongReviewLike.objects.filter(song_review=obj).count()
    
    def get_song_picture(self, obj):
        return obj.song.picture.url if obj.song.picture else None

    class Meta:
        model = models.SongReview
        fields = ['song', 'song_picture', 'content', 'score', 'user', 'user_id', 'likes_count', 'comments_count', 'comments']
    
class SongReviewLikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.SongReviewLike
        fields = ['id']

class SongSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Song
        fields = ['name', 'duration', 'band', 'picture']