from django.db import models
from django.contrib.auth import get_user_model
from django.urls import reverse
from django.utils.translation import gettext_lazy as _

User = get_user_model()

class Band(models.Model):
    name = models.CharField(_("name"), max_length=100)
    # picture = models.ImageField(_("picture"), upload_to='bands/pictures', null=True, blank=True)
    
    class Meta:
        verbose_name = _("band")
        verbose_name_plural = _("bands")

    def __str__(self):
        return f'{self.name}'

    def get_absolute_url(self):
        return reverse("band_detail", kwargs={"pk": self.pk})

class Song(models.Model):
    name = models.CharField(_("name"), max_length=100)
    duration = models.IntegerField(_("duration"))
    band = models.ForeignKey(Band, 
        verbose_name=_("band"), 
        on_delete=models.CASCADE,
        related_name='songs'
        )
    picture = models.ImageField(_("picture"), upload_to='song_reviews/', null=True, blank=True)

    class Meta:
        verbose_name = _("song")
        verbose_name_plural = _("songs")

    def __str__(self):
        return f'{self.name} - {self.band}'

    def get_absolute_url(self):
        return reverse("song_detail", kwargs={"pk": self.pk})

class SongReview(models.Model):
    user = models.ForeignKey(
        User, 
        verbose_name=_("user"), 
        on_delete=models.CASCADE,
        related_name='song_reviews'
        )
    song = models.ForeignKey(Song, 
        verbose_name=_("song"), 
        on_delete=models.CASCADE,
        related_name=('reviews')
        ) 
    content = models.TextField(_("content"), max_length=10000)
    
    SCORE = ((i, f'{i}/10') for i in range(0, 11))
    score = models.PositiveSmallIntegerField(_("score"), choices=SCORE, default=0)

    class Meta:
        verbose_name = _("song review")
        verbose_name_plural = _("song reviews")

    def __str__(self):
        return f'{self.song}: {self.user}'

    def get_absolute_url(self):
        return reverse("songreview_detail", kwargs={"pk": self.pk})

class SongReviewComment(models.Model):
    user = models.ForeignKey(
        User, 
        verbose_name=_("user"), 
        on_delete=models.CASCADE,
        related_name='song_review_comments'
        )
    song_review = models.ForeignKey(
        SongReview, 
        verbose_name=_("song_review"), 
        on_delete=models.CASCADE,
        related_name='comments'
        )
    content = models.TextField(_("content"), max_length=10000)
    
    class Meta:
        verbose_name = _("song review comment")
        verbose_name_plural = _("song review comments")

    def __str__(self):
        return f'{self.song_review}: {self.user}'

    def get_absolute_url(self):
        return reverse("album review comment_detail", kwargs={"pk": self.pk})

class SongReviewLike(models.Model):
    user = models.ForeignKey(
        User, 
        verbose_name=_("user"), 
        on_delete=models.CASCADE,
        related_name='song_review_likes'
        )
    song_review = models.ForeignKey(
        SongReview, 
        verbose_name=_("song_review"), 
        on_delete=models.CASCADE,
        related_name='likes'
        )
    
    class Meta:
        verbose_name = _("song review like")
        verbose_name_plural = _("song review likes")

    def __str__(self):
        return f'{self.song_review}: {self.user}'

    def get_absolute_url(self):
        return reverse("song review like_detail", kwargs={"pk": self.pk})
