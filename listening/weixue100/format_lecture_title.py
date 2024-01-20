import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'toefl_practice.settings')
django.setup()
from listening.models import Lecture

for lecture in Lecture.objects.all():
    title = lecture.title
    title = title.strip()
    title = title[0].upper() + title[1:].lower()
    lecture.title = title
    try:
        lecture.save()
    except django.db.utils.IntegrityError:
        title = '[duplicate] ' + title
        lecture.title = title
        lecture.save()
