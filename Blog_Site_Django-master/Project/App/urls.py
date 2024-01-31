from django.urls import path

from django.contrib.auth.decorators import login_required
from allauth.account.views import LoginView, LogoutView
from django.urls import path
from .views import CustomLoginView
from django.contrib.auth import views as auth_views
from .views import secure
from django.urls import path, include
from .views import CustomLoginView, PostList, PostDetail
urlpatterns = [
    path('', PostList.as_view(), name="home"),
    path('<slug:slug>/', PostList.as_view(), name="post_detail"),
    #path('login/',  auth_views.LoginView.as_view(template_name='login.html'), name='login'),
   # path('accounts/logout/', CustomLogoutView.as_view(), name='logout'),
    path('accounts/login/', CustomLoginView.as_view(), name='login'),
    path('accounts/logout/', LogoutView.as_view(), name='logout'),
    path('accounts/', include('allauth.urls')),
    path('accounts/', include('allauth.socialaccount.urls')),
]
