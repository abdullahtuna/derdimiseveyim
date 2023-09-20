from django.shortcuts import render, redirect
from django.views import generic
from .models import Post
from django.http.response import HttpResponse
from derdimiseveyim.forms import NewUserForm
from django.contrib.auth import login
from django.contrib import messages
from django.shortcuts import render, redirect
from .forms import PostForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404
from django.utils.text import slugify
from django.urls import reverse_lazy
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

# ...

class PostCreate(LoginRequiredMixin, generic.CreateView):
    model = Post
    fields = ["title", "content"]
    template_name = 'post_form.html'

    def get_success_url(self):
        messages.success(
            self.request, 'Derdiniz Başarıyla Sevildi.')
        return reverse_lazy('home')

    def form_valid(self, form):
        obj = form.save(commit=False)
        obj.author = self.request.user
        obj.slug = slugify(form.cleaned_data['title'])
        obj.save()
        return super().form_valid(form)


class PostUpdate(LoginRequiredMixin, generic.UpdateView):
    model = Post
    fields = ["title", "content"]
    template_name = 'post_form.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        update = True
        context['update'] = update

        return context

    def get_success_url(self):
        messages.success(
            self.request, 'Derdiniz Başarıyla Tekrar Sevildi.')
        return reverse_lazy('home')

    def get_queryset(self):
        return self.model.objects.filter(author=self.request.user)


class PostDelete(LoginRequiredMixin, generic.DeleteView):
    model = Post
    template_name = 'post_confirm_delete.html'

    def get_success_url(self):
        messages.success(
            self.request, 'Derdiniz Çöpe Gitti.')
        return reverse_lazy('home')

    def get_queryset(self):
        return self.model.objects.filter(author=self.request.user)
