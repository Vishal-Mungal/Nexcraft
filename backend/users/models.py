from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    email = models.EmailField(unique=True)
    name = models.CharField(max_length=100, blank=True)
    skill_score = models.IntegerField(default=0)
    courses_completed = models.IntegerField(default=0)
    quiz_score = models.IntegerField(default=0)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

class QuizProgress(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    quiz_title = models.CharField(max_length=255)
    score = models.IntegerField()
    timestamp = models.DateTimeField(auto_now_add=True)

class JobApplication(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    company = models.CharField(max_length=100)
    role = models.CharField(max_length=100)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.name} applied to {self.company} - {self.role}"

class LearningProgress(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    topic = models.CharField(max_length=200)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.name} - {self.topic}"
