"""ophtalmo_site URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
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
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from ophtalmo_site.settings import dev
from ophtalmo_center.views import ophtalmo_center_index, ophtalmo_center_details
from ophtalmo_blog.views import ophtalmo_article_index, ophtalmo_article_details
from accounts.views import register,activate, password_reset, reset, login_user,logout_user

urlpatterns = [
    path('ophtalmo_centers', ophtalmo_center_index, name='ophtalmo_center_index'),
    path('ophtalmo_articles', ophtalmo_article_index, name='ophtalmo_article_index'),
    path('admin/', admin.site.urls),
    path('register/', register, name='register'),
    path('activate/<uidb64>/<token>/',activate, name='activate'),
    path('login/', login_user, name='login'),
    path('logout/', logout_user, name='logout'),
    path('login/password_reset/', password_reset, name='password_reset'),
    path('reset/<uidb64>/<token>/', reset, name='reset'),
    path('ophtalmo_articles/<str:slug>/', ophtalmo_article_details,name="ophtalmo_article_details"),
    path('ophtalmo_centers/<str:slug>/', ophtalmo_center_details,name="ophtalmo_center_details"),
    path('ratings/', include('star_ratings.urls', namespace='ratings')),
] + static(dev.MEDIA_URL, document_root=dev.MEDIA_ROOT)