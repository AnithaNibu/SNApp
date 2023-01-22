from django.urls import path
from api import views
urlpatterns=[
    path("appindex",views.appindex,name="appindex"),
    path("register",views.SignupView.as_view(),name="register"),
    path("api/login",views.SigninView.as_view(),name="signin"),
    path("api/home",views.HomeView.as_view(),name='user-home')

]