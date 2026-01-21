from django.db import models
from django.utils import timezone
import datetime
from django.contrib.auth.models import AbstractUser
from django.conf import settings
import uuid   

class User(AbstractUser): 
    is_email_verified = models.BooleanField(default=False) 

    def __str__(self): 
        return self.username 


class Profile(models.Model): 
    user = models.OneToOneField( 
        settings.AUTH_USER_MODEL,  # Use custom user model 
        on_delete=models.CASCADE 
    )
    avatar = models.ImageField( 
        upload_to='avatars/', 
        default='avatars/default.png', 
        blank=True 
    )

    def __str__(self): 
        return f"{self.user.username} Profile" 


class PasswordResetOTP(models.Model): 
    user = models.ForeignKey( 
        settings.AUTH_USER_MODEL,   # Use custom user model
        on_delete=models.CASCADE 
    )
    otp = models.CharField(max_length=6) 
    created_at = models.DateTimeField(auto_now_add=True) 

    def is_valid(self): 
        return timezone.now() < self.created_at + datetime.timedelta(minutes=5) 
    
class EmailVerificationToken(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )
    token = models.UUIDField(default=uuid.uuid4, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"EmailVerificationToken({self.user.username})"