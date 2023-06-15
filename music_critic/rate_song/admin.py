from django.contrib import admin
from .models import *

admin.site.register(Band)
admin.site.register(Song)
admin.site.register(SongReview)
admin.site.register(SongReviewComment)
admin.site.register(SongReviewLike)
