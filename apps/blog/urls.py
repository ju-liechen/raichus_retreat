from django.urls import path

from . import views


app_name = 'blog'
urlpatterns = [
    path('', views.index, name='index'),
    path('posts/', views.BlogView.as_view(), name='posts'),
    path('post/<int:pk>/more', views.PostDetailView.as_view(), name='post_detail'),
]
