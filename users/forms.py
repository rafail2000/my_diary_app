from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserChangeForm, UserCreationForm

from diary.forms import StyleFormMixin
from users.models import User


class UserRegisterForm(StyleFormMixin, UserCreationForm):
    """
    Форма для регистрации пользователя
    """

    password1 = forms.CharField(
        label="Пароль",
        widget=forms.PasswordInput(attrs={"class": "form-control", "placeholder": "Введите пароль"}),
        help_text='<ul class="help-text text-muted small">'
        "<li>• Пароль не должен быть слишком похож на другие ваши личные данные</li>"
        "<li>• Пароль должен содержать минимум 8 символов</li>"
        "<li>• Пароль не должен быть слишком простым и распространённым</li>"
        "<li>• Пароль не должен состоять только из цифр</li>"
        "</ul>",
        error_messages={
            "required": "Это поле обязательно для заполнения.",
        },
    )

    password2 = forms.CharField(
        label="Подтверждение пароля",
        widget=forms.PasswordInput(attrs={"class": "form-control", "placeholder": "Подтвердите пароль"}),
        help_text="Введите тот же пароль ещё раз для проверки.",
        error_messages={
            "required": "Это поле обязательно для заполнения.",
            "password_mismatch": "Пароли не совпадают.",
        },
    )

    class Meta:
        model = User
        fields = ("email", "phone_number", "password1", "password2")
        labels = {
            "email": "Email",
            "phone_number": "Номер телефона",
        }
        widgets = {
            "email": forms.EmailInput(
                attrs={"class": "form-control", "placeholder": "Введите номер телефона (необязательно)"}
            ),
        }
        error_messages = {
            "email": {"required": "Это поле обязательно для заполнения.", "invalid": "Введите корректный email адрес."}
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["phone_number"].required = False

        self.fields["password1"].error_messages = {
            "required": "Это поле обязательно для заполнения.",
            "password_too_short": "Пароль должен содержать минимум 8 символов.",
            "password_too_common": "Пароль не должен быть слишком простым и распространённым.",
            "password_entirely_numeric": "Пароль не должен состоять только из цифр.",
            "password_too_similar": "Пароль не должен быть слишком похож на другие ваши личные данные.",
        }
        self.fields["password2"].error_messages = {
            "required": "Это поле обязательно для заполнения.",
            "password_mismatch": "Пароли не совпадают.",
        }

    def clean_email(self):
        """
        Проверка уникальности email
        """

        email = self.cleaned_data.get("email")
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("Пользователь с таким email уже существует")
        return email


class UserLoginForm(StyleFormMixin, AuthenticationForm):
    """
    Форма для логирования пользователя
    """

    username = forms.EmailField(
        label="Email",
        widget=forms.EmailInput(
            attrs={
                "class": "form-control",
                "placeholder": "Введите ваш email",
                "autofocus": True,
            }
        ),
    )

    password = forms.CharField(
        label="Пароль",
        widget=forms.PasswordInput(attrs={"class": "form-control", "placeholder": "Введите ваш пароль"}),
    )

    error_messages = {
        "invalid_login": "Пожалуйста, введите правильные Email и пароль. Оба поля могут быть чувствительны к регистру.",
        "inactive": "Этот аккаунт неактивен. Пожалуйста, обратитесь к администратору.",
    }

    def confirm_login_allowed(self, user):
        """
        Переопределение сообщения для неактивного аккаунта
        """


class UserUpdateForm(UserChangeForm):
    """
    Форма для редактирования пользователя
    """

    password = None

    class Meta:
        model = User
        fields = ("email", "phone_number")
        labels = {"email": "Email", "phone_number": "Номер телефона"}
        widgets = {
            "email": forms.EmailInput(attrs={"class": "form-control", "placeholder": "Введите email"}),
            "phone_number": forms.TextInput(attrs={"class": "form-control", "placeholder": "Введите номер телефона"}),
        }

    def clean_email(self):
        """
        Проверка уникальности email при редактировании
        """

        email = self.cleaned_data.get("email")
        instance = getattr(self, "instance", None)

        if instance and email != instance.email:
            if User.objects.filter(email=email).exists():
                raise forms.ValidationError("Пользователь с таким email уже существует")
        return email
