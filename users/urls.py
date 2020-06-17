# users/urls.py

from django.urls import path
from users import views as account_views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('signup/', account_views.signup, name='signup'),
    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('', account_views.welcom_view, name='welcom_view'),

    # Edit profile
    path('profile_edit/', account_views.profile_edit, name='profile_edit'),
    path('profile_education/', account_views.profile_education, name='profile_education'),
    path('profile_select_sponsor/', account_views.profile_select_sponsor, name='profile_select_sponsor'),
    path('profile/upload/', account_views.profile_upload_file, name='profile_upload_file'),
    path('profile/reference/', account_views.profile_reference, name='profile_reference'),
    path('profile/summary/', account_views.profile_view, name='profile_summary'),

    # Reference
    path('reference/ref_list/', account_views.ref_list, name='ref_list'),
    path('reference/<uuid:pk>', account_views.ref_upload, name='ref_upload'),

    #path('reference/<uuid:pk>/', account_views.ref_view, name='ref_view'),

    # Sponsor
    path('admin/sponsor/add/', account_views.sponsor_add, name='sponsor_add'),
    path('admin/sponsor/list/', account_views.sponsor_list, name='sponsor_list'),

    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
]