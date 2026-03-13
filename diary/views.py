from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import CreateView, DetailView, ListView, UpdateView, DeleteView

from diary.forms import DiaryForm
from diary.models import Diary
from diary.services import get_title_or_content_list


class DiaryCreateView(LoginRequiredMixin, CreateView):
    """
    Курсор для создания записи
    """

    model = Diary
    form_class = DiaryForm
    template_name = 'diary/diary_form.html'
    success_url = reverse_lazy('diary:diary_list')


class DiaryDetailView(LoginRequiredMixin, DetailView):
    """
    Курсор для просмотра записи
    """

    model = Diary
    template_name = 'diary/diary_item.html'
    context_object_name = 'record'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        pk = self.kwargs.get('pk')
        context['additional_data'] = Diary.objects.get(pk=pk)
        return context


class DiaryListView(LoginRequiredMixin, ListView):
    """
    Курсор для просмотра записей
    """

    model = Diary
    template_name = 'diary/diary_list.html'
    context_object_name = 'records'

    def get_queryset(self):
        search_word = self.request.GET.get('search_word')
        return get_title_or_content_list(search_word)

class DiaryUpdateView(LoginRequiredMixin, UpdateView):
    """
    Курсор для редактирования записи
    """

    model = Diary
    form_class = DiaryForm
    template_name = 'diary/diary_form.html'
    success_url = reverse_lazy('diary:diary_list')


class DiaryDeleteView(LoginRequiredMixin, DeleteView):
    """
    Курсор для удаления записи
    """

    model = Diary
    template_name = 'diary/diary_confirm_delete.html'
    success_url = reverse_lazy('diary:diary_list')
