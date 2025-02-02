from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Postform, Profile,Comments

class Registrationform(UserCreationForm):
    first_name = forms.CharField(required=True)
    last_name = forms.CharField(required=True)
    email = forms.EmailField(required=True)
    username = forms.CharField(required=True)


    class Meta:
        model = User
        fields =  ['first_name', 'last_name', 'username', 'email', 'password1', 'password2']


class Post(forms.ModelForm):
    class Meta:
        model = Postform
        fields = ['title', 'description', 'image']


class commentform(forms.ModelForm):
    class Meta:
        model = Comments
        fields = ['body']


#update profiledetails
class ProfiledetailsUpdateForm(forms.ModelForm):
    first_name = forms.CharField(required=True)
    last_name = forms.CharField(required=True)
    email = forms.EmailField(required=True)

    # Don't include 'username', 'password1', 'password2' for profile update
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']  



# Update profileimage

class ProfileimageUpdateForm(forms.ModelForm):
    
    class Meta:
        model = Profile
        fields = ['image']

