from random import shuffle
from django.db import models

DIFFICULTY = (
    ('easy', 'easy'),
    ('medium', 'medium'),
    ('hard', 'hard'),
)


# Create your models here.
class Quiz(models.Model):
    name = models.CharField(max_length=120)
    topic = models.CharField(max_length=120)
    num_of_questions = models.IntegerField()
    time = models.IntegerField(help_text='duration of duration of the quiz in minutes')
    pass_score = models.IntegerField(help_text='score in %')
    difficulty = models.CharField(max_length=6, choices=DIFFICULTY)

    def __str__(self):
        return f'{__class__.__name__}(name={self.name}, topic={self.topic})'

    def get_questions(self):
        question_list = list(self.question_set.all())
        shuffle(question_list)
        return question_list[:self.num_of_questions]

    class Meta:
        verbose_name_plural = 'Quizes'
