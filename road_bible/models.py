from django.db import models
from django.contrib.auth.models import User

class RoadProgress(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    road = models.CharField(max_length=255)  # You can adjust the max_length as needed
    index = models.PositiveIntegerField()

    def __str__(self):
        print('done')
        return f'{self.user.username} on {self.road} at index {self.index}'
       
