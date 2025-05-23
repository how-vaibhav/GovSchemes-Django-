from django import forms
from django.contrib.auth.models import User
from .models import Feedback, Scheme

class FeedbackForm(forms.ModelForm):
    class Meta:
        model = Feedback
        fields = ['scheme', 'message']
        widgets = {
            'scheme': forms.Select(attrs={'class': 'form-control'})
        }

class AddEmployee(forms.Form):
    username = forms.CharField(max_length=150, label="Enter Username")

class Add_Scheme_Form(forms.ModelForm):

    class Meta:
        model = Scheme
        fields = ['name', 'objective', 'benefits', 'agency', 'full_description', 'gender', 'date_of_birth', 'maritial_status', 'location', 'caste', 'disability', 'minority', 'below_poverty_line', 'income' ]
        widgets = {
            'gender': forms.Select(attrs={'class': 'form-control'}),
            'maritial_status': forms.Select(attrs={'class': 'form-control'}),
            'caste': forms.Select(attrs={'class': 'form-control'}),
        }