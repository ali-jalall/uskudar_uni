from django import forms
from .models import RedSeaUser
from django.contrib.auth.forms import UserCreationForm


class RegisterForm(UserCreationForm):
    class Meta:
        model=RedSeaUser
        fields = ['fullName', 'email', 'phone_number', 'is_student', 'is_club_manager', 'is_sks_admin','password1','password2'] 