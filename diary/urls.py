from django.urls import path

from diary.apps import DiaryConfig
from diary.views import DiaryCreateView, DiaryDeleteView, DiaryDetailView, DiaryListView, DiaryUpdateView

app_name = DiaryConfig.name

urlpatterns = [
    path("new/", DiaryCreateView.as_view(), name="diary_create"),
    path("diary_item/<int:pk>/", DiaryDetailView.as_view(), name="diary_item"),
    path("", DiaryListView.as_view(), name="diary_list"),
    path("<int:pk>/edit/", DiaryUpdateView.as_view(), name="diary_edit"),
    path("<int:pk>/delete/", DiaryDeleteView.as_view(), name="diary_delete"),
]
