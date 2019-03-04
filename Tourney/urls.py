from django.conf import settings
from django.conf.urls.static import static
from django.urls import path

from Tourney import views

app_name = "Tourney"
urlpatterns = [
    path('', views.TournamentViewAll.as_view(), name='tournament-list'),
    path('<int:pk>', views.TournamentView.as_view(), name='tournament-view'),
    path('t_entry/<int:pk>', views.enter_tournament, name='tournament-entry'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
