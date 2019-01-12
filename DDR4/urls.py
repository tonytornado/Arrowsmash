"""DDR4 URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
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
