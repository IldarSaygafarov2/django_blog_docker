from django.urls import path

from . import views

urlpatterns = [
    path('login/', views.show_login_page, name='login'),
    path('registration/', views.show_registration_page, name='registration'),
    path('logout/', views.logout_user, name='logout'),
    path('me/', views.show_profile_page, name='profile-me'),
    path('<str:username>/profile/', views.show_author_profile_page, name='author-profile')
]