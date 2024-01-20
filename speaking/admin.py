from django.contrib import admin
from .models import *


@admin.register(IndependentSp)
class TaskAdmin(admin.ModelAdmin):
    search_fields = ['title']


@admin.register(IntegratedSp)
class IntegratedSpAdmin(admin.ModelAdmin):
    search_fields = ['title']
