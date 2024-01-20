from django.contrib import admin
from django.contrib.auth.models import Permission
from django.contrib.contenttypes.models import ContentType

admin.site.site_url = "/"
admin.site.site_header = admin.site.site_title = "TOEFL practice"
admin.site.index_title = "Home"


@admin.register(ContentType)
class ContentTypeAdmin(admin.ModelAdmin):
    list_filter = ['app_label']


@admin.register(Permission)
class PermissionAdmin(admin.ModelAdmin):
    list_display = ['name', 'content_type', 'codename']
    list_filter = ['content_type']
