from django.contrib import admin

from diary.models import Diary


@admin.register(Diary)
class ContactAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'content', 'user', 'publication_date')
    list_filter = ('publication_date',)
    search_fields = ('title', 'content', 'user')
