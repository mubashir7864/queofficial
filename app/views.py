from django.shortcuts import render,redirect
from django.contrib import messages
from .models import Postform
from .forms import Registrationform , Post
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login,logout,authenticate


# Create your views here.

@login_required(login_url='/login')
def home(request):
    posts = Postform.objects.all()
    return render(request, 'app/home.html', {'posts': posts})



# sign up view

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


#create post view

@login_required(login_url='/login')
def createpost(request):
    if request.method == 'POST':
        form = Post(request.POST, request.FILES)
        if form.is_valid():
           post = form.save(commit=False)
           post.author = request.user 
           post.save()
           return redirect('/home')
    else:
        form = Post()
    
    return render(request, 'app/createpost.html', {'form': form})

