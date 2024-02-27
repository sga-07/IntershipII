from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone
from cryptography.fernet import Fernet
from django.contrib.auth.signals import user_logged_in, user_logged_out
STATUS = ((0, "Draft"), (1, "Published"))

class Post(models.Model):
    id = models.BigAutoField(primary_key=True)
    title = models.CharField(max_length=200, unique=True)
    slug = models.SlugField(max_length=200, unique=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='blog_posts')
    created_on = models.DateTimeField(default=timezone.now)
    updated_on = models.DateTimeField(auto_now=True)
    content = models.TextField()
    encrypted_content = models.BinaryField(null=True, default=None)
    status = models.IntegerField(choices=STATUS, default=0)
    key = models.BinaryField(null=True)  # Add a field to store the encryption key

    class Meta:
        ordering = ['-created_on']

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if self.content:
            key = Fernet.generate_key()
            cipher_suite = Fernet(key)
            self.encrypted_content = cipher_suite.encrypt(self.content.encode())
            self.key = key  # Store the encryption key
        super().save(*args, **kwargs)

    def decrypt_content(self):
        if self.encrypted_content and self.key:
            cipher_suite = Fernet(self.key)
            decrypted_content = cipher_suite.decrypt(self.encrypted_content).decode()
            return decrypted_content
        return ""

from django.utils import timezone

class MyModel(models.Model):
    my_field = models.DateTimeField(default=timezone.now)


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.userprofile.save()


class UserProfile(models.Model):
    id = models.BigAutoField(primary_key=True)  # Specify primary key
    user = models.OneToOneField(User, on_delete=models.CASCADE)

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.userprofile.save()

class UserActivity(models.Model):
    id = models.BigAutoField(primary_key=True)  # Specify primary key
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    activity_type = models.CharField(max_length=10)  # 'login' or 'logout'
    timestamp = models.DateTimeField(auto_now_add=True)

@receiver(user_logged_in)
def user_logged_in_handler(sender, request, user, **kwargs):
    UserActivity.objects.create(user=user, activity_type='login')

@receiver(user_logged_out)
def user_logged_out_handler(sender, request, user, **kwargs):
    UserActivity.objects.create(user=user, activity_type='logout')