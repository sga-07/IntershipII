from django.contrib import admin

# Register your models here.
from .models import Post
from .models import UserActivity
from .models import UserProfile

class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'slug', 'status', 'created_on')
    list_filter = ('status',)
    search_fields = ['title', 'content']


admin.site.register(Post, PostAdmin)
admin.site.register(UserActivity)
admin.site.register(UserProfile)

