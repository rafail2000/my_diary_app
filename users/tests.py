from io import StringIO

from django.core.management import call_command
from django.test import TestCase
from django.urls import reverse

from users.forms import UserRegisterForm, UserUpdateForm
from users.models import User


class UserTestCase(TestCase):
    """
    Тестирование модели пользователя
    """

    def setUp(self):
        self.user = User(email="user@example.com", phone_number="88888888888")
        self.user.set_password("user@password")
        self.user.save()

    def test_user_data(self):
        """
        Тесты данных пользователя при регистрации
        """

        user = User.objects.get(email="user@example.com")
        self.assertEqual(user.email, "user@example.com")
        self.assertEqual(user.phone_number, "88888888888")
        self.assertTrue(user.check_password("user@password"))
        self.assertEqual(str(user), "user@example.com")

    def test_user_create_view_context(self):
        """
        Тесты контекста в UserCreateView
        """

        response = self.client.get(reverse("users:register"))
        self.assertEqual(response.status_code, 200)
        self.assertIn("title", response.context)
        self.assertEqual(response.context["title"], "Регистрация")
        self.assertTemplateUsed(response, "users/user_form.html")

    def test_user_update_view_context(self):
        """
        Тесты контекста в UserUpdateView
        """

        self.client.login(email="user@example.com", password="user@password")
        response = self.client.get(reverse("users:user_edit", args=[self.user.pk]))
        self.assertEqual(response.status_code, 200)
        self.assertIn("title", response.context)
        self.assertEqual(response.context["title"], "Редактирование профиля")
        self.assertTemplateUsed(response, "users/user_form.html")

    def test_user_update_view_get_objects(self):
        """
        Тесты метода get_objects
        """

        self.client.login(email="user@example.com", password="user@password")
        response = self.client.get(reverse("users:user_edit", args=[self.user.pk]))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context["user"], self.user)

    def test_register_with_new_email(self):
        """
        Тесты валидации для нового email
        """

        form_data = {
            "email": "newuser@example.com",
            "password1": "newuser@password",
            "password2": "newuser@password",
        }
        form = UserRegisterForm(data=form_data)
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data["email"], "newuser@example.com")

    def test_register_duplicate_email(self):
        """
        Тесты дублирования email
        """

        form_data = {
            "email": "user@example.com",
            "password1": "user@password",
            "password2": "user@password",
        }
        form = UserRegisterForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn("email", form.errors)
        self.assertEqual(
            form.errors["email"][0],
            "Пользователь с таким email уже существует"
        )

    def test_update_form_email(self):
        """
        Тесты на обновление email существующего пользователя
        """

        form_data = {
            "email": "updateuser@example.com",
        }
        form = UserUpdateForm(data=form_data, instance=self.user)
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data["email"], "updateuser@example.com")

    def test_update_form_duplicate_email(self):
        """
        Тесты обновление email на такой же
        """

        self.other_user = User(email="exist_user@example.com", phone_number="88888888888")
        self.other_user.set_password("exist_user@password")
        self.other_user.save()

        form_data = {
            "email": "exist_user@example.com",
        }
        form = UserUpdateForm(data=form_data, instance=self.user)
        self.assertFalse(form.is_valid())
        self.assertIn("email", form.errors)
        self.assertEqual(
            form.errors["email"][0],
            "Пользователь с таким email уже существует"
        )


class CreateSuperUserCommand(TestCase):
    """
    Тесты для проверки кастомной команды csu.py
    """
    def test_command_creates_superuser(self):
        """
        Тесты создания суперпользователя
        """

        self.assertEqual(User.objects.filter(email="admin@mail.ru").count(), 0)

        out = StringIO()
        call_command("csu", stdout=out)

        self.assertEqual(User.objects.filter(email="admin@mail.ru").count(), 1)

        user = User.objects.get(email="admin@mail.ru")
        self.assertEqual(user.first_name, "Admin")
        self.assertEqual(user.last_name, "Admin")
        self.assertTrue(user.is_staff)
        self.assertTrue(user.is_superuser)
        self.assertTrue(user.check_password("1234"))
