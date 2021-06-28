from django.contrib import admin
from .models import Question, Answer


class AnswerInline(admin.TabularInline):
    model = Answer


class QuestionAdmin(admin.ModelAdmin):
    inlines = [AnswerInline]


# Register your models here.
admin.site.register(Question, QuestionAdmin)
admin.site.register(Answer)
