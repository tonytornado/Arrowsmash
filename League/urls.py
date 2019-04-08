from django.conf import settings
from django.conf.urls.static import static
from django.urls import path

from League import views

app_name = "League"
urlpatterns = [
    path('', views.LeagueViewAll.as_view(), name='league-list'),
    path('<int:pk>', views.LeagueView.as_view(), name='league-view'),
    path('t_entry/<int:pk>', views.enter_league, name='league-entry'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
