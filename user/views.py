from django.urls import reverse_lazy
from django.views import generic

from user.forms import SignUpForm


# Create your views here.
class SignUpView(generic.CreateView):
    form_class = SignUpForm
    success_url = reverse_lazy("login")
    template_name = "registration/signup.html"
