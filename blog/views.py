from django.shortcuts import render, redirect
from django.views import generic
from .models import Post
from derdimiseveyim.forms import NewUserForm
from django.contrib.auth import login
from django.contrib import messages

class PostList(generic.ListView):
    queryset = Post.objects.filter(status=1).order_by('-created_on')
    template_name = 'index.html'

class PostDetail(generic.DetailView):
    model = Post
    template_name = 'post_detail.html'


# Create your views here.
