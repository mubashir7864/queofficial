from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class Registrationform(UserCreationForm):
    first_name = forms.CharField(required=True)
    last_name = forms.CharField(required=True)
    email = forms.EmailField(required=True)
    username = forms.CharField(required=True) 

    class Meta:
        model = User
        fields =  ['first_name', 'last_name', 'username', 'email', 'password1', 'password2']



