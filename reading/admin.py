from django.contrib import admin
from .models import *
from django import forms
from django.db.models.query import QuerySet


class ChoicesModelForm(forms.ModelForm):
    class Meta:
        model = ReadingQuestion
        fields = "__all__"
        widgets = {
            'choice_a': forms.Textarea(attrs={'rows': 2, 'cols': '100%'}),
            'choice_b': forms.Textarea(attrs={'rows': 2, 'cols': '100%'}),
            'choice_c': forms.Textarea(attrs={'rows': 2, 'cols': '100%'}),
            'choice_d': forms.Textarea(attrs={'rows': 2, 'cols': '100%'}),
            'choice_e': forms.Textarea(attrs={'rows': 2, 'cols': '100%'}),
            'choice_f': forms.Textarea(attrs={'rows': 2, 'cols': '100%'}),
            'question': forms.Textarea(attrs={'rows': 4, 'cols': '100%'}),
            'listen_again': RichTextField(config_name='reading_question_citation'),
        }


class ReadingQuestionInline(admin.StackedInline):
    model = ReadingQuestion
    form = ChoicesModelForm
    extra = 1
    fieldsets = [
        (None, {"fields": ["idx", "question", "answer"]}),
        ("Advanced options", {"fields": ["passage", "citation", "choice_a", "choice_b",
                                         "choice_c", "choice_d", "choice_e", "choice_f"],
                              "classes": ["collapse"]})
    ]


class NQuestionsFilter(admin.SimpleListFilter):
    title = 'Number of questions'
    parameter_name = 'n_questions'

    def lookups(self, request, model_admin):
        passages = Passage.objects.all()
        counts = sorted({p.n_questions for p in passages})
        return [(count, count) for count in counts]

    def queryset(self, request, queryset):
        if self.value():
            passages = Passage.objects.all()
            value = int(self.value())
            filtered_passages_id = [p.id for p in passages if p.n_questions == value]
            filtered_passages = passages.filter(id__in=filtered_passages_id)
            filtered_questions = queryset.filter(passage__id__in=filtered_passages)
            return filtered_questions
        else:
            return queryset


@admin.register(Passage)
class PassageAdmin(admin.ModelAdmin):
    search_fields = ['title']
    inlines = [ReadingQuestionInline]


@admin.register(ReadingQuestion)
class ReadingQuestionAdmin(admin.ModelAdmin):
    list_filter = [NQuestionsFilter, 'idx', ('citation', admin.EmptyFieldListFilter)]
    autocomplete_fields = ['passage']
    search_fields = ['passage__title']


@admin.register(ReadingAnswer)
class ReadingAnswersAdmin(admin.ModelAdmin):
    list_filter = ['user__username', 'created_time']
    list_display = ['created_time', 'question']
    autocomplete_fields = ['user', 'question']
    search_fields = ['question__passage__title']
