from django.shortcuts import render,redirect,get_object_or_404
from django.contrib import messages
from .models import Postform, Profile
from .forms import Registrationform , Post , ProfiledetailsUpdateForm, ProfileimageUpdateForm
from django.contrib.auth.decorators import login_required,permission_required
from django.contrib.auth import login,logout,authenticate


# Create your views here.

@login_required(login_url='/login')
def home(request):
    posts = Postform.objects.all()

    if request.method == 'POST':
        post_id = request.POST.get("post-id")
        post = Postform.objects.filter(id=post_id).first()
        if post and (post.author == request.user or request.user.has_perm('app.delete_Postform')):
            post.delete()

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
# @permission_required("app.add_Postform", login_url="/login" , raise_exception=True)
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



@login_required(login_url='/login')
def updateprofile(request):
    
    user = request.user

    # Ensure profile exists
    if not hasattr(user, 'profile'):
        Profile.objects.create(user=user)


    if request.method == 'POST':
        imgform = ProfileimageUpdateForm(request.POST, request.FILES, instance=request.user.profile)
        profileform = ProfiledetailsUpdateForm(request.POST,  instance=request.user)
        if imgform.is_valid() and profileform.is_valid():
            profileform.save()
            imgform.save()
            return redirect('/home')
        else:
            # Debugging: Print form errors in console
            print("Profile Form Errors:", profileform.errors)
            print("Image Form Errors:", imgform.errors)
    else:
        imgform = ProfileimageUpdateForm(instance=request.user.profile)
        profileform = ProfiledetailsUpdateForm(instance=request.user)

    return render(request, 'app/updateuser.html' , {'profileform': profileform , 'imgform' : imgform})


# my posts rendering

@login_required(login_url='/login')
def mypost(request):
    user = request.user
    myposts = Postform.objects.filter(author = user)

    return render(request,'app/myposts.html', {'myposts' : myposts})


# # updating posts

# @login_required(login_url='/login')
# def updatepost(request, post_id):
#     if request.method == 'POST':
#         # post_id = request.POST.get("post-id")
#         # post = Postform.objects.get(id = post_id)
#         if post and (post.author == request.user or request.user.has_perm('app.change_Postform')):
#             form = Post(request.POST,request.FILES, instance=post)
#             if form.is_valid():
#                 form.save()
#                 return redirect('myposts')
#      else:
#         form = Post(instance=post)
        
#     return render(request, 'app/updatepost.html',  {'form': form , 'post' : post})




@login_required(login_url='/login')
def updatepost(request, post_id):
    post = get_object_or_404(Postform, id=post_id) 
    
    # Restrict update access
    if post.author != request.user and not request.user.has_perm('app.change_Postform'):
        return redirect('home')

    if request.method == 'POST':
        form = Post(request.POST, request.FILES, instance=post)  
        if form.is_valid():
            form.save()
            return redirect('myposts')
    else:
        form = Post(instance=post)

    return render(request, 'app/updatepost.html', {'form': form, 'post': post})
