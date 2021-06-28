from django.db import models
from django.contrib.auth.models import User
from quizes.models import Quiz


# Create your models here.
class Result(models.Model):
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    score = models.FloatField()

    def __str__(self):
        return f'{__class__.__name__}(pk={self.pk})'
