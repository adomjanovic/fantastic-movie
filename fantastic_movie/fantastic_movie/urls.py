"""fantastic_movie URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
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
from django.contrib import admin
from django.urls import path
from App1 import views
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('registration/', views.registration, name='registration'),
    path('login/', auth_views.login, name='login'),
    path('logout/', auth_views.logout, name='logout'),
    path('change-password/',auth_views.PasswordChangeView.as_view(template_name='registration/change-password.html'), name='changePassword'),
    path('change-password-done/',auth_views.PasswordChangeDoneView.as_view(template_name='registration/change-password-done.html'), name='password_change_done'),
    path('API/', views.API, name='movie_fetch'),
    path('movies/<int:id>/', views.details),
    path('movies/edit/<int:id>/', views.edit, name='editMovie'),
	path('movies/delete/<int:id>/', views.delete, name='deleteMovie'),
	path('movies/new', views.new, name='newMovie'),
	path('movies/', views.index, name='movies'),
	path('movies/search', views.search, name='searchMovie'),
    
    # ajax
    path('moviesAjax', views.Ajax.as_view(), name="ajax"),

] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

