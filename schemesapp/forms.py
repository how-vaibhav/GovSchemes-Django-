from django import forms
from django.contrib.auth.models import User
from .models import Feedback

class FeedbackForm(forms.ModelForm):
    class Meta:
        model = Feedback
        fields = ['scheme', 'message']
        widgets = {
            'scheme': forms.Select(attrs={'class': 'form-control'})
        }

class AddEmployee(forms.Form):
    username = forms.CharField(max_length=150, label="Enter Username")
