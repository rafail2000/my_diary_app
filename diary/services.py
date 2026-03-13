from django.db.models import Q

from diary.models import Diary


def get_title_or_content_list(search_word=None):
    """
    Получает список записей по заголовку или контенту.
    """

    data = Diary.objects.all()

    if search_word:
        data = data.filter(Q(title__icontains=search_word) | Q(content__icontains=search_word))

    return data.order_by('-publication_date')