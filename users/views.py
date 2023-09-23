from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy
from django.views import generic
from django.contrib import messages


class SignUpView(generic.CreateView):
    form_class = UserCreationForm
    template_name = "signup.html"
    def get_success_url(self):
        messages.success(self.request, 'Üyelik işleminiz tamamlandı. Giriş yapabilirsiniz.')
        return reverse_lazy('login')
# Create your views here.
