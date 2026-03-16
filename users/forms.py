from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django import forms

from diary.forms import StyleFormMixin
from users.models import User


class UserRegisterForm(StyleFormMixin, UserCreationForm):
    """
    Форма для регистрации пользователя
    """

    password1 = forms.CharField(
        label="Пароль",
        widget=forms.PasswordInput(attrs={
            "class": "form-control",
            "placeholder": "Введите пароль"
        }),
        help_text='<ul class="help-text text-muted small">'
                    '<li>• Пароль не должен быть слишком похож на другие ваши личные данные</li>'
                    '<li>• Пароль должен содержать минимум 8 символов</li>'
                    '<li>• Пароль не должен быть слишком простым и распространённым</li>'
                    '<li>• Пароль не должен состоять только из цифр</li>'
                    '</ul>'
    )

    password2 = forms.CharField(
        label="Подтверждение пароля",
        widget=forms.PasswordInput(attrs={
            "class": "form-control",
            "placeholder": "Подтвердите пароль"
        }),
        help_text="Введите тот же пароль ещё раз для проверки."
    )

    class Meta:
        model = User
        fields = ('email', 'phone_number', 'password1', 'password2')
        labels = {
            "email": "Email",
            "phone_number": "Номер телефона",
        }
        widgets = {
            "email": forms.EmailInput(attrs={
                "class": "form-control",
                "placeholder": "Введите номер телефона (необязательно)"
            }),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["phone_number"].required = False

        self.fields["password1"].error = {
            "password_too_short": "Пароль должен содержать минимум 8 символов.",
            "password_to_common": "Пароль не должен быть слишком простым и распространённым.",
            "password_too_common": "Пароль не должен состоять только из цифр.",
            "password_too_similar": "Пароль не должен быть слишком похож на другие ваши личные данные.",
        }
        self.fields["password2"].error_messages = {
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


class UserUpdateForm(UserChangeForm):
    """
    Форма для редактирования пользователя
    """

    password = None

    class Meta:
        model = User
        fields = ("email", "phone_number")
        labels = {
            "email": "Email",
            "phone_number": "Номер телефона"
        }
        widgets = {
            "email": forms.EmailInput(attrs={
                "class": "form-control",
                "placeholder": "Введите email"
            }),
            "phone_number": forms.TextInput(attrs={
                "class":"form-control",
                "placeholder": "Введите номер телефона"
            }),
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
