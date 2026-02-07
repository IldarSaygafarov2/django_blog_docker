from django.urls import path

from . import views

#http://127.0.0.1:800/
urlpatterns = [
    path('', views.show_home_page, name='home'),
    path('contacts/',views.contacts_view, name='contacts'),
    path('categories/<int:pk>/', views.show_post_by_category, name='category-posts'),
    path('post/<int:pk>/', views.show_post_detail_page, name='post-detail'),
    path('posts/<int:pk>/delete/', views.PostDeleteView.as_view(),name ='post-delete'),
    path('posts/<int:pk>/update/', views.PostUpdateView.as_view(),name ='post-update'),
    path('posts,<int:pk>/<str:action>/', views.add_like_or_dislike, name = 'add-vote'),
    path('comments/<int:comment_id>/delete/', views.delete_comment, name ='delete-comment'),
    path('create/', views.create_post, name='create'),
    path('search/', views.search_posts, name='search')
]