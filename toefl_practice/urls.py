"""
URL configuration for toefl_practice project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.conf.urls.static import static
from django.conf import settings
import practice.views as v1
import my_admin.views as v2
import reading.views as v3
import listening.views as v4

urlpatterns = [
    path('admin/', admin.site.urls),
    path('login', v2.view_login),
    path('add_login', v2.add_login),
    path('delete_login', v2.delete_login),

    path('', v1.app_center),

    path('view_reading', v3.view_reading),
    path('add_answer_reading', v3.answer_reading),

    path('view_listening', v4.view_lecture),
    path('add_answer_listening', v4.answer_listening)
]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
