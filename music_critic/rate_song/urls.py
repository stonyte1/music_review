from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.SongReviewList.as_view()),
    path('<int:pk>', views.SongReviewDetail.as_view()),
    path('<int:song_review_pk>/comment/', views.SongReviewCommentList.as_view()),
    path('comment/<int:pk>', views.SongReviewCommentDetail.as_view()),
    path('<int:pk>/like', views.SongReviewLikeCreateDestroy.as_view()),
    path('<int:pk>/song', views.SongDetail.as_view()),
] + (static(settings.STATIC_URL, document_root=settings.STATIC_ROOT) \
   + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT))
