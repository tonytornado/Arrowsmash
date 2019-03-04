from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.urls import path

from Accounts import views

app_name = "Accounts"
urlpatterns = [
    path('admin/', admin.site.urls, name='single_akumu_shinjen'),
    path('update_profile', views.update_profile, name='update-profile'),
    path('login/', auth_views.LoginView.as_view(template_name='registration/login.html'),
         name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='home'), name='logout'),
    # path('accounts/', include('django.contrib.auth.urls')),
] \
    # + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
