from accounts import views
from django.contrib.auth.views import LoginView
from django.urls import path


app_name = "accounts"

urlpatterns = [
    path("signup/", views.signup_view, name="signup"),
    path("login/", LoginView.as_view(), name="login"),
    path("logout/", views.logout_view, name="logout"),
]
