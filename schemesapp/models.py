from django.db import models
from django.contrib.auth.models import User

# Create your models here.

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

    GENDER_CHOICES = [
    ('M' ,'Male'),
    ('F' ,'Female'),
    ('T', "Transgender")
    ]

    MARITIAL_CHOICES = [
    ('MARRIED' ,'Married'),
    ('NOT MARRIED' ,'Never Married'),
    ('WIDOWED', "Widowed"),
    ('DIVORCEE', "Divorcee")
    ]

    CASTE_CHOICES = [
    ('G' ,'General'),
    ('OBC' ,'Other Backward Caste(OBC)'),
    ('PVTG', "Particularly Vulnarable Tribal Group"),
    ('SC', "Scheduled Class"),
    ('ST', "Scheduled Tribe")
    ]

    gender= models.CharField(max_length=50, choices=GENDER_CHOICES, blank=True, null=True)
    min_age = models.IntegerField(blank=True, null=True)
    maritial_status = models.CharField(max_length=50, choices=MARITIAL_CHOICES, blank=True, null=True)
    location = models.CharField(max_length=100, choices=[('rural', "Rural"),('urban', "Urban")], blank=True, null=True)
    caste = models.CharField(max_length=100, choices=CASTE_CHOICES, blank=True, null=True)
    disability = models.BooleanField(default=False, blank=True, null=True)
    minority = models.BooleanField(default=False, blank=True, null=True)
    below_poverty_line = models.BooleanField(default=False, blank=True, null=True)
    income = models.PositiveIntegerField(blank=True, null=True)

    def __str__(self):
        return self.name

class UserDetails(models.Model):
    GENDER_CHOICES = [
    ('M' ,'Male'),
    ('F' ,'Female'),
    ('T', "Transgender")
    ]

    MARITIAL_CHOICES = [
    ('MARRIED' ,'Married'),
    ('NOT MARRIED' ,'Never Married'),
    ('WIDOWED', "Widowed"),
    ('DIVORCEE', "Divorcee")
    ]

    CASTE_CHOICES = [
    ('G' ,'General'),
    ('OBC' ,'Other Backward Caste(OBC)'),
    ('PVTG', "Particularly Vulnarable Tribal Group"),
    ('SC', "Scheduled Class"),
    ('ST', "Scheduled Tribe")
    ]


    user = models.OneToOneField(User, on_delete=models.CASCADE, default=0)
    name = models.CharField(max_length=255)
    email = models.EmailField()
    gender= models.CharField(max_length=50, choices=GENDER_CHOICES)
    age = models.IntegerField()
    maritial_status = models.CharField(max_length=50, choices=MARITIAL_CHOICES)
    location = models.CharField(max_length=100, choices=[('rural', "Rural"),('urban', "Urban")])
    caste = models.CharField(max_length=100, choices=CASTE_CHOICES)
    disability = models.BooleanField()
    minority = models.BooleanField()
    below_poverty_line = models.BooleanField()
    income = models.PositiveIntegerField()

class Feedback(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    scheme = models.ForeignKey(Scheme, on_delete=models.CASCADE, null=True, blank=True)
    reply = models.TextField(blank=True, null=True)
    message = models.TextField()
    submitted_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Feedback by {self.user.username}"
    