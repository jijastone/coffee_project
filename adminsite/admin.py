from django.contrib import admin
from django.utils.text import slugify
from unidecode import unidecode

from .models import (Course, Lecture, Test,
                     LearningProgress, LectureMaterial, Question, Answer)


admin.site.register(LectureMaterial)
admin.site.register(Question)
admin.site.register(Answer)