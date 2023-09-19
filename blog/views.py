from django.shortcuts import render, redirect
from django.views import generic
from .models import Post
from django.http.response import HttpResponse
from derdimiseveyim.forms import NewUserForm
from django.contrib.auth import login
from django.contrib import messages


def about(request):
    return render(request, 'about.html')
def iletisim(request):
    return render(request, 'iletisim.html')
def kurallar(request):
    return render(request, 'kurallar.html')

class PostList(generic.ListView):
    queryset = Post.objects.filter(status=1).order_by('-created_on')
    template_name = 'index.html'

class PostDetail(generic.DetailView):
    model = Post
    template_name = 'post_detail.html'




# Create your views here.
