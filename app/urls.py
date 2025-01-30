from django.urls import path
from django.contrib.auth import views as auth_views
from . import views


urlpatterns = [
    path('home/', views.home , name= 'home'),
    path('', views.home , {}),
    path('signup/', views.signup, name='signup' ),
    path("login/", auth_views.LoginView.as_view(template_name="registration/login.html"), name="login")
]
