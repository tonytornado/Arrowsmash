from django.conf import settings
from django.conf.urls.static import static
from django.urls import path

from Scores import views

app_name = 'Scores'
urlpatterns = [
    # path('admin/', admin.site.urls),
    path('', views.ScoreListing.as_view(), name='score-list'),
    path('detail/<int:pk>', views.ScoreDetail.as_view(), name='score-detail'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
