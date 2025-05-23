from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Feedback(models.Model):
    #For now using predefined choices, once we put schemes in data base we can edit it to take schemes from database 
    SCHEME_CHOICES = [
        ('BBBP' ,'Beti Bacho Beti Padau'),
        ('SBA' ,'Swach Bharat Abhiyan'),
        ('NIL', "General")
    ]
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    scheme = models.CharField(max_length=50, choices=SCHEME_CHOICES, default='NIL')
    reply = models.TextField(blank=True, null=True)
    message = models.TextField()
    submitted_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Feedback by {self.user.username}"
    

class Notification(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    message = models.CharField(max_length=255)
    link = models.URLField(blank=True,null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

class Scheme(models.Model):
    name = models.CharField(max_length=255)
    objective = models.TextField()
    benefits = models.TextField()
    agency = models.CharField(max_length=255)
    full_description = models.TextField(blank=True, null=True) 

    def __str__(self):
        return self.name