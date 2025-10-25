import datetime

from django.db import models
from django.utils import timezone

# Creació Model Question

class Question(models.Model):
    question_text = models.CharField(max_length=200)
    pub_date = models.DateTimeField("date published")
    #Funció per poder veure la informació dels camps del model
    def __str__(self):
        return self.question_text
    #Funció per poder veure la TimeZone
    def was_published_recently(self):
        return self.pub_date >= timezone.now() - datetime.timedelta(days=1)

# Creació Model Choice

class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)
    #Veure la informació dels camps del model
    def __str__(self):
        return self.choice_text

