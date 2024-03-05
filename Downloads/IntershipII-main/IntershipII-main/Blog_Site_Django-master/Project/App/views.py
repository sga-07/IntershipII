from django.contrib.auth.decorators import login_required
#from django.shortcuts import render
#from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
#from .models import Post
from django.contrib.auth.views import LoginView, LogoutView
from django.urls import reverse_lazy
from cryptography.fernet import Fernet
from django.shortcuts import render
from django.views import generic
from .models import Post, UserProfile

from django.http import HttpResponseForbidden

from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.backends import default_backend

def get_private_key_manually():
    """
    Prompt the user to enter their private key manually.
    """
    private_key_str = input("Enter your private key: ")

    try:
        # Decode the private key string
        private_key_bytes = private_key_str.encode()
        private_key = serialization.load_pem_private_key(private_key_bytes, password=None, backend=default_backend())
        return private_key
    except Exception as e:
        print("Error: Invalid private key format.")
        return None

class PostDetail(LoginRequiredMixin, generic.DetailView):
    model = Post
    template_name = 'post_detail.html'

    def test_func(self):
        post = self.get_object()
        return self.request.user == post.author

    def is_post_creator(self, user, post):
        # Check if the given user is the creator of the post
        return user == post.author

    # def get(self, request, *args, **kwargs):
    #     if not self.test_func():
    #         return HttpResponseForbidden("You are not authorized to view this content.")
    #     return super().get(request, *args, **kwargs)

    # def get_context_data(self, **kwargs):
    #     context = super().get_context_data(**kwargs)
    #     post = self.get_object()
    #     context['is_author'] = self.is_post_creator(self.request.user, post)
    #     return context
    def get(self, request, *args, **kwargs):
        post = self.get_object()
        private_key = get_private_key_manually()
        if private_key and not self.request.user == post.author:
            return HttpResponseForbidden("You are not authorized to view this content.")

        context = self.get_context_data(object=post)
        if private_key:
            decrypted_content = post.decrypt_content(private_key)
            context['decrypted_content'] = decrypted_content
        return self.render_to_response(context)
def is_user_post_creator(user, post):
    # Check if the given user is the creator of the post
    return user == post.author

def is_user_post_creator_based_on_activity_and_profile(user, post):
    # Check if the given user is the creator of the post based on user activity and profile
    user_activities = UserActivity.objects.filter(user=user, activity_type='login').order_by('-timestamp')
    if user_activities.exists():
        last_login_activity = user_activities.first()
        if last_login_activity.timestamp > post.created_on:
            # The user logged in after the post was created, so they couldn't have created the post
            return False

    # Check user profile to ensure they have necessary permissions
    try:
        user_profile = UserProfile.objects.get(user=user)
        # Add additional checks on user profile if necessary
    except UserProfile.DoesNotExist:
        # User profile doesn't exist, which might indicate they can't be the post creator
        return False

    # Check if the user is the creator of the post based on other criteria if needed
    return is_user_post_creator(user, post)

# class PostDetail(LoginRequiredMixin, generic.DetailView):
#     model = Post
#     template_name = 'post_detail.html'

#     def test_func(self):
#         post = self.get_object()
#         return self.request.user == post.author

#     def get(self, request, *args, **kwargs):
#         if not self.test_func():
#             return HttpResponseForbidden("You are not authorized to view this content.")
#         return super().get(request, *args, **kwargs)

#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         post = self.get_object()
#         context['is_author'] = self.request.user == post.author
#         return context

# class PostDetail(LoginRequiredMixin, generic.DetailView):
#     model = Post
#     template_name = 'post_detail.html'

#     def test_func(self):
#         post = self.get_object()
#         return self.request.user == post.author

#     def get(self, request, *args, **kwargs):
#         if not self.test_func():
#             return HttpResponseForbidden("You are not authorized to view this content.")
#         return super().get(request, *args, **kwargs)

#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         post = self.get_object()
#         decrypted_content = post.decrypt_content()
#         context['decrypted_content'] = decrypted_content
#         context.pop('author', None)
#         context.pop('created_on', None)
#         return context
    
# class PostDetail(LoginRequiredMixin, generic.DetailView):
#     model = Post
#     template_name = 'post_detail.html'
#
#     def test_func(self):
#         post = self.get_object()
#         # Check if the logged-in user is the author of the post
#         return self.request.user == post.author
#
#     def get(self, request, *args, **kwargs):
#         # Check permissions before accessing the post detail
#         if not self.test_func():
#             return HttpResponseForbidden("You are not authorized to view this content.")
#         return super().get(request, *args, **kwargs)
#
#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         post = self.get_object()
#         decrypted_content = post.decrypt_content()
#         context['decrypted_content'] = decrypted_content
#         return context
# class PostDetail(UserPassesTestMixin, generic.DetailView):
#     model = Post
#     template_name = 'post_detail.html'
#
#     # def get_context_data(self, **kwargs):
#     #     context = super().get_context_data(**kwargs)
#     #     post = self.get_object()
#     #     decrypted_content = post.decrypt_content()
#     #     context['decrypted_content'] = decrypted_content
#     #     return context
#     #
#     # def test_func(self):
#     #     # Check if the logged-in user is a superuser
#     #     if self.request.user.is_superuser:
#     #         return True
#     #     else:
#     #         post = self.get_object()
#     #         # Check if the post author is a superuser
#     #         if post.author.is_superuser:
#     #             return False
#     #         return True
#     def get(self, request, *args, **kwargs):
#         self.object = self.get_object()
#         if not self.test_func():
#             return HttpResponseForbidden("You don't have permission to view this post.")
#         context = self.get_context_data(object=self.object)
#         return self.render_to_response(context)
#
#     def dispatch(self, request, *args, **kwargs):
#         if self.request.user != self.get_object().author:
#             return HttpResponseForbidden("You are not authorized to view this post.")
#         return super().dispatch(request, *args, **kwargs)
    # def test_func(self):
    #     # Check if the logged-in user is a superuser
    #     if self.request.user.is_superuser:
    #         return True
    #     else:
    #         post = self.get_object()
    #         # Check if the post author is the logged-in user
    #         if post.author == self.request.user:
    #             return True
    #         else:
    #             # Deny access if the logged-in user is not the author
    #             return False
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
