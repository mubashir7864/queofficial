from django.shortcuts import render,redirect
from django.contrib import messages
from .forms import Registrationform 
from django.contrib.auth import login,logout,authenticate


# Create your views here.


def home(request):
    return render(request, 'app/home.html', {})

def signup(request):
    if request.method == 'POST':
        form = Registrationform(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Account created successfully! Please log in.")  
            return redirect('login')  # Redirect user to login
        else:
            messages.error(request, "Please correct the errors below.")  # Show errors if form is invalid

    else:
        form = Registrationform()

    return render(request, 'registration/signup.html', {'form': form})
