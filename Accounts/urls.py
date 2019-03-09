from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

from Accounts import views

app_name = "Accounts"
urlpatterns = [
    path('admin/', admin.site.urls, name='single_akumu_shinjen'),
    path('update_profile', views.update_profile, name='update-profile'),
    path('register', views.register, name='register'),
    path('profile/', include([
        path('', views.ProfileListing.as_view(), name='profile-list'),
        path('<int:pk>/', views.ProfileView.as_view(), name='view-profile'),
        path('follow/<int:pk>', views.follower_add, name='follow'),
        path('unfollow/<int:pk>', views.follower_delete, name='unfollow'),
    ])),
]
    # + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
