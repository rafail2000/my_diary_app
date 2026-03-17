from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView, UpdateView

from .forms import UserRegisterForm, UserUpdateForm
from .models import User


class UserCreateView(SuccessMessageMixin, CreateView):
    """
    Курсор создания пользователя
    """

    model = User
    form_class = UserRegisterForm
    template_name = "users/user_form.html"
    success_url = reverse_lazy("users:login")
    success_message = "Регистрация прошла успешно!"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Регистрация"
        return context


class UserUpdateView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    """
    Курсор редактирования пользователя
    """

    model = User
    form_class = UserUpdateForm
    template_name = "users/user_form.html"
    success_url = reverse_lazy("diary:diary_list")
    success_message = "Профиль успешно обновлён"
    login_url = "users:login"

    def get_object(self, queryset=None):
        """
        Возвращает текущего пользователя
        """

        return self.request.user

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Редактирование профиля"
        return context
