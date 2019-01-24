from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

from Accounts import views

urlpatterns = [
    path('', views.home, name='home'),
    path('admin/', admin.site.urls, name='double_akumu_shinjen'),
    path('profile/', views.ProfileListing.as_view(), name='profile-list'),
    path('profile/<int:pk>/', views.ProfileView.as_view(), name='view-profile'),
    path('scores/', include('Scores.urls', namespace='Scores')),
    path('tournaments/', include('Tourney.urls', namespace='Tourney')),
    path('register/', views.register, name='register'),
    path('accounts/', include('Accounts.urls', namespace='Accounts')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
