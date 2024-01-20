from django.contrib import admin
from .models import *


@admin.register(IntegratedWt)
class IntegratedWtAdmin(admin.ModelAdmin):
    search_fields = ['title']


@admin.register(AcDiscussion)
class AcDiscussionAdmin(admin.ModelAdmin):
    search_fields = ['title']
