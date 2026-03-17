from django.contrib.auth.views import LoginView, LogoutView
from django.urls import path

from users.apps import UsersConfig
from users.forms import UserLoginForm
from users.views import UserCreateView, UserUpdateView

app_name = UsersConfig.name

urlpatterns = [
    path(
        "login/", LoginView.as_view(template_name="users/login.html", authentication_form=UserLoginForm), name="login"
    ),
    path("logout/", LogoutView.as_view(), name="logout"),
    path("register/", UserCreateView.as_view(template_name="users/user_form.html"), name="register"),
    path("<int:pk>/edit/", UserUpdateView.as_view(), name="user_edit"),
]
