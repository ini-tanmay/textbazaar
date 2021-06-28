from django.shortcuts import render
from django.views import generic
from .models import Post

class PostList(generic.ListView):
    queryset = Post.objects.order_by('-created_on')
    template_name = 'blog/blog.html'

class PostDetail(generic.DetailView):
    model = Post
    template_name = 'blog/post_detail.html'
