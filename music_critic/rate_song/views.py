from django.shortcuts import render
from rest_framework import generics, permissions, mixins, status
from rest_framework.response import Response
from . import models, serializers
from django.utils.translation import gettext_lazy as _
from rest_framework.exceptions import ValidationError


class SongReviewList(generics.ListCreateAPIView):
    queryset = models.SongReview.objects.all()
    serializer_class = serializers.SongReviewSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class SongReviewDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = models.SongReview.objects.all()
    serializer_class = serializers.SongReviewSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def put(self, request, *arg, **kwargs):
        song_review = models.SongReview.objects.filter(
            pk=kwargs['pk'],
            user=self.request.user
        )
        if song_review.exists():
            return self.update(request, *arg, **kwargs)
        else: 
            raise ValidationError(_('You have no right to edit this!'))

    def delete(self, request, *args, **kwargs):
        song_review = models.SongReview.objects.filter(
            pk=kwargs['pk'],
            user=self.request.user
        )
        if song_review.exists():
            return self.destroy(request, *args, *kwargs)
        else:
            raise ValidationError(_('You have no right to delete this!'))

class SongReviewCommentList(generics.ListCreateAPIView):
    serializer_class = serializers.SongReviewCommentSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        song_review = models.SongReview.objects.get(pk=self.kwargs['song_review_pk'])
        serializer.save(user=self.request.user, song_review=song_review)
    
    def get_queryset(self):
        song_review = models.SongReview.objects.get(pk=self.kwargs['song_review_pk'])
        return models.SongReviewComment.objects.filter(song_review=song_review)

class SongReviewCommentDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = models.SongReviewComment.objects.all()
    serializer_class = serializers.SongReviewCommentSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def put(self, request, *arg, **kwargs):
        try:
            comment = models.SongReviewComment.objects.get(
                pk=kwargs['pk'], 
                user=self.request.user
                )
        except Exception as e:
            raise ValidationError(_('You cannot update this.'))
        else:
            return self.update(request, *arg, **kwargs)
        
    def delete(self, request, *arg, **kwargs):
        try:
            comment = models.SongReviewComment.objects.get(
                pk=kwargs['pk'], 
                user=self.request.user)
        except Exception as e:
            raise ValidationError(_('You cannot delete this'))
        else: 
            return self.destroy(request, *arg, **kwargs)
        
class SongReviewLikeCreateDestroy(generics.CreateAPIView, mixins.DestroyModelMixin):
    serializer_class = serializers.SongReviewLikeSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        song_review = models.SongReview.objects.get(pk=self.kwargs['pk'])
        return models.SongReviewLike.objects.filter(song_review=song_review)
    
    def perform_create(self, serializer):
        if self.get_queryset().exists():
            raise ValidationError(_('You already liked this'))
        song_review = models.SongReview.objects.get(pk=self.kwargs['pk'])
        serializer.save(user=self.request.user, song_review=song_review)
    
    def delete(self, request, *args, **kwargs):
        if self.get_queryset().exists():
            self.get_queryset().delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        else: 
            return ValidationError(_('You cannot unlike what you don\'t like'))

class SongDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = models.Song.objects.all()
    serializer_class = serializers.SongSerializer
    permission_classes = [permissions.IsAdminUser]
