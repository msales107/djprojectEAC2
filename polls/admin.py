from django.contrib import admin
#Importar model Question i Choice al Panell de Admin
from .models import Question
from .models import Choice

admin.site.register(Question)
admin.site.register(Choice)
