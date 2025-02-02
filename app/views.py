from django.shortcuts import render,redirect,get_object_or_404
from django.contrib import messages
from .models import Postform, Profile
from .forms import Registrationform , Post , ProfiledetailsUpdateForm, ProfileimageUpdateForm
from django.contrib.auth.decorators import login_required,permission_required
from django.contrib.auth.views import PasswordResetView
from django.contrib.auth.models import Group
from django.urls import reverse
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth import get_user_model
from django.shortcuts import render, get_object_or_404

User = get_user_model()


# reset password 

class CustomPasswordResetView(PasswordResetView):
    def form_valid(self, form):
        email = form.cleaned_data.get("email")
        try:
            user = User.objects.get(email=email)
            uid = urlsafe_base64_encode(force_bytes(user.pk))
            token = default_token_generator.make_token(user)
            reset_url = self.request.build_absolute_uri(reverse("password_reset_confirm", kwargs={"uidb64": uid, "token": token}))

            return render(self.request, "registration/password_reset_link.html", {"reset_url": reset_url})
        except User.DoesNotExist:
            pass  # Do nothing for invalid emails to avoid user enumeration attacks
        return super().form_valid(form)

# //////////////
# Create your views here.

@login_required(login_url='/login')
def home(request):
    posts = Postform.objects.all().order_by('-created_at')
    users = User.objects.exclude(is_superuser = True)
    




    if request.method == 'POST':
        user_id = request.POST.get("user-id")
        post_id = request.POST.get("post-id")

        
        if post_id:
            post = Postform.objects.filter(id=post_id).first()
            if post and (post.author == request.user or request.user.has_perm('app.delete_Postform')):
                post.delete()       
          
        elif 'ban-user' in request.POST:
            user = User.objects.get(id=user_id)
            
            if user and request.user.is_staff:
                try:
                    group, created = Group.objects.get_or_create(name='usersdefault')
                    group.user_set.remove(user)
                    messages.success(request, f"{user.username} has been banned.")
                except:
                    pass
            else:
                messages.error(request, "User not found.")
        
        # Delete User
        elif 'delete-user' in request.POST:
            user = User.objects.get(id=user_id)
            if user and user != request.user:  # Ensure a user can't delete themselves
                user.delete()
                messages.success(request, "User deleted successfully.")
            else:
                messages.error(request, "You can't delete yourself or the user does not exist.")

        return redirect('home') 

    return render(request, 'app/home.html', {'posts': posts , 'users' : users, })



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
@permission_required("app.add_postform", raise_exception=True)
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
@permission_required("app.change_postform", raise_exception=True)
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
