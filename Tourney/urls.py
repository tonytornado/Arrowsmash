from django.conf.urls.static import static
from django.urls import path

from DDR4 import settings
from Tourney import views

app_name = "Tourney"
urlpatterns = [
    path('', views.TournamentViewAll.as_view(), name='tournament-list'),
    path('tournament/<int:pk>', views.TournamentView.as_view(), name='tournament-view'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
