from django.views import generic
from .models import Post, Comment
from .forms import CommentForm, ContactForm
from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404
from django.utils.text import slugify
from django.urls import reverse_lazy
from django.contrib import messages

def about(request):
    return render(request, 'about.html')
def iletisim(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()
            return render(request, 'success_iletisim.html')
    form = ContactForm()
    context = {'form': form}
    return render(request, 'iletisim.html', context)
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
        messages.success(self.request, 'Derdiniz onay için Yöneticilerimize gönderildi.')
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
        messages.success(self.request, 'Derdiniz Başarıyla Düzenlendi.')
        return reverse_lazy('home')

    def get_queryset(self):
        return self.model.objects.filter(author=self.request.user)


class PostDelete(LoginRequiredMixin, generic.DeleteView):
    model = Post
    template_name = 'post_confirm_delete.html'

    def get_success_url(self):
        messages.success(self.request, 'Derdiniz Çöpe Gitti.')
        return reverse_lazy('home')

    def get_queryset(self):
        return self.model.objects.filter(author=self.request.user)

class PostView(generic.DetailView):
    model = Post
    template_name = 'post_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        pk = self.kwargs["pk"]
        slug = self.kwargs["slug"]

        form = CommentForm()
        post = get_object_or_404(Post, pk=pk, slug=slug)
        comments = post.comment_set.all()

        context['post'] = post
        context['comments'] = comments
        context['form'] = form
        return context

    def post(self, request, *args, **kwargs):
        form = CommentForm(request.POST)
        self.object = self.get_object()
        context = super().get_context_data(**kwargs)

        post = Post.objects.filter(id=self.kwargs['pk'])[0]
        comments = post.comment_set.all()

        context['post'] = post
        context['comments'] = comments
        context['form'] = form

        if form.is_valid():
            name = self.request.user
            content = form.cleaned_data['content']

            comment = Comment.objects.create(
                name=name, content=content, post=post
            )

            form = CommentForm()
            context['form'] = form
            return self.render_to_response(context=context)


        return self.render_to_response(context=context)
