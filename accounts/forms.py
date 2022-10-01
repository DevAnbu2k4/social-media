from distutils.command.upload import upload
from attr import fields
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from . models import UserProfile
from django.forms.models import ModelForm
from django.forms.widgets import FileInput


class UserRegistrationForm(UserCreationForm):
    first_name = forms.CharField(max_length=101)
    last_name = forms.CharField(max_length=101)
    email = forms.EmailField() 
  

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'password1', 'password2']

class EditProfileForm(forms.ModelForm):
    profile_Picture = forms.ImageField(required=True)
    Bio =  forms.CharField(widget=forms.TextInput(), max_length=50, required=False)
        
    class Meta:
        model = UserProfile
        fields = ['profile_Picture', 'Bio']
