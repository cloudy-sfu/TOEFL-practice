from django.contrib import admin
from .models import *
from django import forms


class ChoicesModelForm(forms.ModelForm):
    class Meta:
        model = ListeningQuestion
        fields = "__all__"
        widgets = {
            'choice_a': forms.Textarea(attrs={'rows': 2, 'cols': '100%'}),
            'choice_b': forms.Textarea(attrs={'rows': 2, 'cols': '100%'}),
            'choice_c': forms.Textarea(attrs={'rows': 2, 'cols': '100%'}),
            'choice_d': forms.Textarea(attrs={'rows': 2, 'cols': '100%'}),
            'choice_e': forms.Textarea(attrs={'rows': 2, 'cols': '100%'}),
            'choice_f': forms.Textarea(attrs={'rows': 2, 'cols': '100%'}),
            'question': forms.Textarea(attrs={'rows': 2, 'cols': '100%'}),
            'listen_again': forms.ClearableFileInput(),
        }


class ListeningQuestionInline(admin.StackedInline):
    model = ListeningQuestion
    form = ChoicesModelForm
    extra = 1
    fieldsets = [
        (None, {"fields": ["idx", "question", "answer"]}),
        (
            "Advanced options",
            {"fields": ["lecture", "listen_again", "choice_a", "choice_b",
                        "choice_c", "choice_d", "choice_e", "choice_f"],
             "classes": ["collapse"]}
        ),
    ]


class NQuestionsFilter(admin.SimpleListFilter):
    title = 'Number of questions'
    parameter_name = 'n_questions'

    def lookups(self, request, model_admin):
        lectures = Lecture.objects.all()
        counts = sorted({p.n_questions for p in lectures})
        return [(count, count) for count in counts]

    def queryset(self, request, queryset):
        if self.value():
            lectures = Lecture.objects.all()
            value = int(self.value())
            filtered_lectures_id = [p.id for p in lectures if p.n_questions == value]
            filtered_lectures = lectures.filter(id__in=filtered_lectures_id)
            filtered_questions = queryset.filter(passage__id__in=filtered_lectures)
            return filtered_questions
        else:
            return queryset


@admin.register(Lecture)
class LectureAdmin(admin.ModelAdmin):
    list_filter = [('original_text', admin.EmptyFieldListFilter)]
    search_fields = ['title']
    ordering = ['title']
    inlines = [ListeningQuestionInline]


@admin.register(ListeningQuestion)
class ListeningQuestionAdmin(admin.ModelAdmin):
    list_filter = [NQuestionsFilter, 'idx']
    autocomplete_fields = ['lecture']
    search_fields = ['lecture__title']


@admin.register(ListeningAnswer)
class ListeningAnswerAdmin(admin.ModelAdmin):
    list_filter = ['user__username', 'created_time']
    list_display = ['created_time', 'question']
    autocomplete_fields = ['user', 'question']
    search_fields = ['question__lecture__title']
