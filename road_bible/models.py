from django.contrib.auth.models import User
from django.db import models

class UserProgress(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    current_sentence_index = models.IntegerField(default=0)
    hidden_word_indices = models.TextField(default="")
