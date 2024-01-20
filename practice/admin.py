from django.contrib import admin
from .models import *


@admin.register(Practice)
class PracticeAdmin(admin.ModelAdmin):
    filter_horizontal = ['reading_list', 'listening_list']
    autocomplete_fields = ['speaking_1', 'speaking_2', 'speaking_3', 'speaking_4',
                           'writing_1', 'writing_2']
    search_fields = ['speaking_1', 'speaking_2', 'speaking_3', 'speaking_4', 'writing_1',
                     'writing_2']
