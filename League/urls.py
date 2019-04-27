from django.conf import settings
from django.conf.urls.static import static
from django.urls import path, include

from League import views

app_name = "League"
urlpatterns = [
    path('l/', include([
        path('', views.LeagueViewAll.as_view(), name='league-list'),
        path('MakeLeague', views.LeagueCreate.as_view(), name='league-add'),
        path('<int:pk>', views.LeagueView.as_view(), name='league-view'),
        path('<int:pk>/league_entry', views.enter_league, name='league-entry')
    ])),
    path('t/', include([
        path('', views.TrialViewAll.as_view(), name='trial-list'),
        path('<int:pk>', views.TrialView.as_view(), name='trial-view'),
        path('<int:pk>/trial_entry', views.add_trial, name='trial-entry'),
    ])),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
