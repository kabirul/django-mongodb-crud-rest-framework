from django.shortcuts import render
from django.http.response import JsonResponse
from django.http import HttpResponse
from rest_framework.parsers import JSONParser 
from rest_framework import status
from django.urls import reverse

from .models import Blog 
from blogs.serializers import BlogSerializer
from rest_framework.decorators import api_view

@api_view(['GET', 'POST', 'DELETE'])
def blog_list(request):   
    if request.method == 'GET':
        blogs = Blog.objects.all()
        
        title = request.GET.get('title', None)
        if title is not None:
            blogs = blogs.filter(title__icontains=title)
        
        blogs_serializer = BlogSerializer(blogs, many=True)
        return JsonResponse(blogs_serializer.data, safe=False) 

    elif request.method == 'POST':
        blog_data = JSONParser().parse(request)
        blog_serializer = BlogSerializer(data=blog_data)

        if blog_serializer.is_valid():
            blog_serializer.save()
            return JsonResponse(blog_serializer.data, status=status.HTTP_201_CREATED) 
        return JsonResponse(blog_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        count = Blog.objects.all().delete()
        return JsonResponse({'message': '{} Blogs were deleted successfully!'.format(count[0])}, status=status.HTTP_204_NO_CONTENT)
    
 
@api_view(['GET', 'PUT', 'DELETE'])
def blog_detail(request, pk):
    try: 
        blog = Blog.objects.get(id=pk) 
    except Blog.DoesNotExist: 
        return JsonResponse({'message': 'The blogs does not exist'}, status=status.HTTP_404_NOT_FOUND) 
 
    if request.method == 'GET': 
        blog_serializer = BlogSerializer(blog) 
        return JsonResponse(blog_serializer.data) 
 
    elif request.method == 'PUT': 
        blog_data = JSONParser().parse(request) 
        blog_serializer = BlogSerializer(blog, data=blog_data) 
        if blog_serializer.is_valid(): 
            blog_serializer.save() 
            return JsonResponse(blog_serializer.data) 
        return JsonResponse(blog_serializer.errors, status=status.HTTP_400_BAD_REQUEST) 
 
    elif request.method == 'DELETE': 
        blog.delete() 
        return JsonResponse({'message': 'Blog was deleted successfully!'}, status=status.HTTP_204_NO_CONTENT)
   
         
@api_view(['GET'])
def blog_list_published(request):

    blogs = Blog.objects.filter(published=True)
        
    if request.method == 'GET': 
        blogs_serializer = BlogSerializer(blogs, many=True)
        return JsonResponse(blogs_serializer.data, safe=False)
    return JsonResponse({'message': 'GET list of blogs, POST a new blog, DELETE all blogs'}) 