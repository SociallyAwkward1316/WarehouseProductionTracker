from django import forms
from django.contrib.auth.models import User
from .models import UserProfile, Shift, Downtime

class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    shift_type = forms.ChoiceField(choices=UserProfile.SHIFT_CHOICES)
    job_type = forms.ChoiceField(choices=UserProfile.JOB_CHOICES)

    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'shift_type', 'job_type']


class ShiftForm(forms.ModelForm):
    
    class Meta:
        model = Shift
        fields = ['duty']


class ShiftUpdateForm(forms.ModelForm):
    class Meta:
        model = Shift
        fields = ['move_type']


class DowntimeForm(forms.ModelForm):
    class Meta:
        model = Downtime
        fields = ['reason', 'duration']