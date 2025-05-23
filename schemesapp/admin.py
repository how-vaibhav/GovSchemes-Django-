from django.contrib import admin
from .models import Feedback, Notification, Scheme
# Register your models here.
admin.site.register(Feedback)
admin.site.register(Notification)
admin.site.register(Scheme)