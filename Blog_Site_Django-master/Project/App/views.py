from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView, LogoutView
from .models import Post
from django.contrib.auth.views import LoginView
from django.urls import reverse_lazy

class CustomLoginView(LoginView):
    template_name = 'login.html'


    def get_success_url(self):
        # Redirect users to the target site after a successful login
        return reverse_lazy('home')

# Create your views here.

 # Specify the context variable name for the list of posts
class PostList(LoginRequiredMixin, generic.ListView):
    queryset = Post.objects.filter(status=1).order_by('-created_on')
    template_name = 'index.html'
@login_required

def secure(request):
    return render(request,"home.html",{})
class PostDetail(LoginRequiredMixin,generic.DetailView):
    model = Post
    template_name = 'post_detail.html'


