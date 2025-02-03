from django.urls import path
from django.contrib.auth import views as auth_views
from . import views
from .views import CustomPasswordResetView


urlpatterns = [
    path('home/', views.home , name= 'home'),
    path('', views.home , {}),
    path('signup/', views.signup, name='signup' ),
    path('createpost/', views.createpost,name='createpost'),
    path('updateprofile/', views.updateprofile, name='updateprofile'),
    path('myposts/', views.mypost, name ='myposts'),
    path('updatepost/<int:post_id>/', views.updatepost , name='updatepost'),
    path("login/", auth_views.LoginView.as_view(template_name="registration/login.html"), name="login"),
    path("password_reset/",CustomPasswordResetView.as_view(template_name="registration/resetpassword.html"), name="password_reset"),
    path("password_reset/done/", auth_views.PasswordResetDoneView.as_view(template_name="registration/passwordresetdone.html"), name="password_reset_done"),
    path("reset/<uidb64>/<token>/", auth_views.PasswordResetConfirmView.as_view(template_name="registration/resetconfirm.html"), name="password_reset_confirm"),
    path("reset/done/", auth_views.PasswordResetCompleteView.as_view(template_name="registration/resetcomplete.html"), name="password_reset_complete"),




]
