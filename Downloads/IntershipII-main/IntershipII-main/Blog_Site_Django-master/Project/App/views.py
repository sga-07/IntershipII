from django.contrib.auth.decorators import login_required
#from django.shortcuts import render
#from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin
#from .models import Post
from django.contrib.auth.views import LoginView, LogoutView
from django.urls import reverse_lazy
from cryptography.fernet import Fernet
from django.shortcuts import render
from django.views import generic
from .models import Post

class PostDetail(generic.DetailView):
    model = Post
    template_name = 'post_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        post = self.get_object()
        decrypted_content = post.decrypt_content()
        context['decrypted_content'] = decrypted_content
        return context

class CustomLoginView(LoginView):
    template_name = 'login.html'

    def get_success_url(self):
        # Redirect users to the target site after a successful login
        return reverse_lazy('home')

# Specify the context variable name for the list of posts
class PostList(LoginRequiredMixin, generic.ListView):
    queryset = Post.objects.filter(status=1).order_by('-created_on')
    template_name = 'index.html'

    def get_queryset(self):
        queryset = super().get_queryset()
        # Decrypt content for each post
        for post in queryset:
            post.content = post.decrypt_content()
        return queryset

@login_required
def secure(request):
    return render(request,"home.html",{})

# class PostDetail(LoginRequiredMixin, generic.DetailView):
#     model = Post
#     template_name = 'post_detail.html'
#
#     def get_object(self, queryset=None):
#         obj = super().get_object(queryset)
#         # Decrypt content for the post
#         obj.content = obj.decrypt_content()
#         return obj
