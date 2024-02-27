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
from django.http import HttpResponseForbidden
from django.contrib.auth.mixins import LoginRequiredMixin

def superuser_required(function=None):
    actual_decorator = user_passes_test(
        lambda u: u.is_active and u.is_superuser,
        login_url='/login/?next=' + reverse_lazy('login')
    )
    if function:
        return actual_decorator(function)
    return actual_decorator
class PostDetail(generic.DetailView):
    model = Post
    template_name = 'post_detail.html'

    # def get_context_data(self, **kwargs):
    #     context = super().get_context_data(**kwargs)
    #     post = self.get_object()
    #     decrypted_content = post.decrypt_content()
    #     context['decrypted_content'] = decrypted_content
    #     return context
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        post = self.get_object()

        # Check if the user is a superuser or the author of the post
        if self.request.user.is_superuser or self.request.user == post.author:
            decrypted_content = post.decrypt_content()
            context['decrypted_content'] = decrypted_content
        else:
            context['decrypted_content'] = None  # Hide content for regular users

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