from datetime import datetime

from django.db import models
from django.db.models import Avg
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils.text import slugify
from unidecode import unidecode



class Course(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    video_url = models.URLField(blank=True)
    course_slug = models.SlugField(unique=True, max_length=100, default='')


    def save(self, *args, **kwargs):
        if not self.course_slug or self.course_slug != slugify(unidecode(self.title)):
            self.course_slug = slugify(unidecode(self.title))
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title


@receiver(post_save, sender=Course)
def create_learning_progress(sender, instance, created, **kwargs):
    if created:
        users = instance.users.all()
        for user in users:
            LearningProgress.objects.create(user=user, course=instance)


class Lecture(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField()
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    lecture_slug = models.SlugField(unique=True, max_length=100, default='')

    def save(self, *args, **kwargs):
        if not self.lecture_slug or self.lecture_slug != slugify(unidecode(self.title)):
            self.lecture_slug = slugify(unidecode(self.title))
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title


class Test(models.Model):
    title = models.CharField(max_length=100)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    test_slug = models.SlugField(unique=True, max_length=100, default='')

    def save(self, *args, **kwargs):
        if not self.test_slug or self.test_slug != slugify(unidecode(self.title)):
            self.test_slug = slugify(unidecode(self.title))
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title


class Question(models.Model):
    test = models.ForeignKey(Test, on_delete=models.CASCADE)
    question_text = models.CharField(max_length=250)

    def __str__(self):
        return self.question_text


class Answer(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    answer_text = models.CharField(max_length=250)
    is_correct = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.question} - {self.answer_text}"


class LearningProgress(models.Model):
    user = models.ForeignKey('employees.UserProfile', on_delete=models.CASCADE)
    course = models.ForeignKey('courses.Course', on_delete=models.CASCADE)
    completion_percentage = models.IntegerField(default=0)
    start_date = models.DateTimeField(default=datetime.now)
    end_date = models.DateTimeField(default=datetime.now)
    is_complete = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        if self.completion_percentage == 100:
            self.is_complete = True
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.user}-{self.course}"



class LectureMaterial(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    content = models.TextField()
    material_link = models.URLField(null=True, default='')

    def __str__(self):
        return self.course.title