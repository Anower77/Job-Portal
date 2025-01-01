from django.contrib.auth.models import AbstractUser
from django.db import models
from .managers import CustomUserManager

class CustomUser(AbstractUser):
    GENDER_CHOICES = [
        ('male', 'Male'),
        ('female', 'Female'),
        ('other', 'Other')
    ]
    
    ROLE_CHOICES = [
        ('employer', 'Employer'),
        ('employee', 'Job Seeker')
    ]

    username = None
    email = models.EmailField(unique=True)
    role = models.CharField(max_length=10, choices=ROLE_CHOICES)
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES)
    cv_link = models.URLField(
        max_length=500, 
        blank=True,
        help_text="Your CV link (Google Drive or other)"
    )
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    # New profile fields
    phone_number = models.CharField(max_length=15, blank=True)
    linkedin_profile = models.URLField(max_length=255, blank=True)
    personal_website = models.URLField(max_length=255, blank=True)
    city = models.CharField(max_length=100, blank=True)
    country = models.CharField(max_length=100, blank=True)
    date_of_birth = models.DateField(null=True, blank=True)
    profile_picture = models.ImageField(upload_to='profile_pictures/', blank=True)
    nationality = models.CharField(max_length=100, blank=True)
    work_eligibility = models.BooleanField(default=False)
    languages = models.CharField(max_length=255, blank=True, help_text="Comma separated languages")
    github_profile = models.URLField(max_length=255, blank=True)
    
    def get_full_name(self):
        return f"{self.first_name} {self.last_name}"

    def __str__(self):
        return self.email
