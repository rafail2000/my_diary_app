from django.db import models


class Diary(models.Model):
    """
    Класс дневника
    """

    title = models.CharField(max_length=200, verbose_name="Заголовок", help_text="Введите заголовок")
    content = models.TextField(null=True, blank=True, verbose_name="Запись", help_text="Введите запись")
    user = models.ForeignKey(
        "users.User",
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        related_name="diary",
        verbose_name="Автор",
        help_text="Введите автора",
    )
    publication_date = models.DateTimeField(
        auto_now_add=True, verbose_name="Дата записи", help_text="Введите дату записи"
    )

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "запись"
        verbose_name_plural = "записи"
        ordering = [
            "-publication_date",
        ]
