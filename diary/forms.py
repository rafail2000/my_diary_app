from django.forms import ModelForm, BooleanField

from diary.models import Diary


class StyleFormMixin:
    """
    Класс Mixin для стилизации формы
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, fild in self.fields.items():
            if isinstance(fild, BooleanField):
                fild.widget.attrs['class'] = "form-check-input"
            else:
                fild.widget.attrs['class'] = "form-control"


class DiaryForm(StyleFormMixin, ModelForm):
    """
    Класс формы дневника
    """

    class Meta:
        model = Diary
        fields = '__all__'
