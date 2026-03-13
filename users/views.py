from django.urls import reverse_lazy
from django.views.generic.edit import CreateView, UpdateView

from .forms import UserRegisterForm
from .models import User


class UserCreateView(CreateView):
    """
    Курсор создания пользователя
    """

    model = User
    form_class = UserRegisterForm
    success_url = reverse_lazy('users:login')


class UserUpdateView(UpdateView):
    """
    Курсор редактирования пользователя
    """

    model = User
    form_class = UserRegisterForm
    template_name = 'users/user_form.html'
    success_url = reverse_lazy('diary:diary_list')
