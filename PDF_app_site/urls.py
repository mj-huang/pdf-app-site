"""PDF_app_site URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
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
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static 

urlpatterns = [
    path('admin/', admin.site.urls, name='admin'),
    path('pdf/', include('allauth.urls')),
    
    # Local apps
    path('pdf/', include('users.urls')),

    #path('signup/', account_views.signup, name='signup'),
    #path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    #path('profile/edit/', account_views.profile_edit, name='profile_edit'),
    #path('profile/upload/', account_views.profile_upload_file, name='profile_upload_file'),
    #path('profile/reference/', account_views.profile_reference, name='profile_reference'),
    #path('profile/summary/', account_views.profile_view, name='profile_summary'),
    #path('logout/', auth_views.LogoutView.as_view(), name='logout'),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

#if settings.DEBUG:
#    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

 #path('profile/<int:pk>/', account_views.view_profile, name='view_profile'),
    #path('profile/nav/', account_views.profile_nav, name='profile_nav'),