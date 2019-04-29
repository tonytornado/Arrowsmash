from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.urls import path, include

from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('s/', include('Scores.urls', namespace='Scores')),
    path('l/', include('League.urls', namespace='League')),
    path('a/', include('Accounts.urls', namespace='Accounts')),
    path('accounts/', include([
        path('admin/', admin.site.urls, name="access-panel"),
        path('login/', auth_views.LoginView.as_view(template_name='registration/login.html'), name='login'),
        path('logout/', auth_views.LogoutView.as_view(next_page='home'), name='logout'),
    ])),
    path('info/', include([
        path('about', views.about, name='about'),
        path('contact', views.contact, name='contact'),
        path('contribute', views.contribute, name='contribute')
    ])),

    # path('feed/', views.FeedSet.as_view(), name='live-feed'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
