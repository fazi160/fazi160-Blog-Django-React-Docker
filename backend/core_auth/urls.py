from django.urls import path
from . import views
urlpatterns = [
    path('home/', views.HomeView.as_view(), name ='home'),
    path('logout/', views.LogoutView.as_view(), name ='logout'),
    path('withoutauth/',views.CheckWithoutPermission.as_view(), name='without_auth'),
    path('register/', views.UserRegister.as_view(), name='register'),
]