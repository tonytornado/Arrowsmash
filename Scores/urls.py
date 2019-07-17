from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns

from Scores import views

app_name = 'Scores'
urlpatterns = [
    path('', views.ScoreListing.as_view(), name='score-list'),
    path('detail/<int:pk>', views.ScoreDetail.as_view(), name='score-detail'),
    path('submit', views.ScoreSubmit.as_view(), name='score-submit'),
    # path('jsonpretty/', views.JSONView.as_view(), name='json-pretty'),
    # path('songDB/', views.SongDB.as_view(), name='dbview'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

urlpatterns = format_suffix_patterns(urlpatterns)
