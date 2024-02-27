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
from django.contrib.auth.mixins import UserPassesTestMixin

class PostDetail(UserPassesTestMixin, generic.DetailView):
    model = Post
    template_name = 'post_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        post = self.get_object()
        decrypted_content = post.decrypt_content()
        context['decrypted_content'] = decrypted_content
        return context

    def test_func(self):
        # Check if the logged-in user is a superuser
        if self.request.user.is_superuser:
            return True
        else:
            post = self.get_object()
            # Check if the post author is a superuser
            if post.author.is_superuser:
                return False
            return True

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

from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Post, UserActivity


# Function to print users who logged in and users who created posts
def print_login_and_post_creator_users():
    # Get all login activities
    login_activities = UserActivity.objects.filter(activity_type='login')

    print("Users who logged in:")
    for activity in login_activities:
        print(activity.user.username)

    print("\nUsers who created posts:")
    post_creators = User.objects.filter(blog_posts__isnull=False).distinct()
    for user in post_creators:
        print(user.username)


# View to display posts
from django.shortcuts import render


def post_list(request):
    print_login_and_post_creator_users()  # Print users who logged in and post creators
    posts = Post.objects.filter(status=1).order_by('-created_on')
    return render(request, 'post_list.html', {'posts': posts})


# Signal handler to print users when a post is created
@receiver(post_save, sender=Post)
def print_users_on_post_creation(sender, instance, created, **kwargs):
    if created:
        print_login_and_post_creator_users()
