from django.urls import path
from .import views


urlpatterns = [      
   
    path('api/blogs/', views.blog_list, name='blog-list'),
    path('api/blogs/<int:pk>', views.blog_detail, name='blog-detail'),
    path('api/blogs/published', views.blog_list_published, name='blog-list-published')

]