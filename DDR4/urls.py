from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

from Accounts import views

urlpatterns = [
    path('', views.home, name='home'),
    path('admin/', admin.site.urls),
    path('p/', views.ProfileListing.as_view(), name='profile-list'),
    path('p/<int:pk>/', views.ProfileView.as_view(), name='view-profile'),
    path('p/follow/<int:pk>', views.follower_add, name='follow'),
    path('p/unfollow/<int:pk>', views.follower_delete, name='unfollow'),
    path('s/', include('Scores.urls', namespace='Scores')),
    path('t/', include('Tourney.urls', namespace='Tourney')),
    path('register/', views.register, name='register'),
    path('a/', include('Accounts.urls', namespace='Accounts')),
    # path('feed/', views.FeedSet.as_view(), name='live-feed'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
