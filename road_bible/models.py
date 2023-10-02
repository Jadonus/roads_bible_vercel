from django.db import models

class RoadProgress(models.Model):
    user_name = models.CharField(max_length=255)  # Add a field for user name
    road = models.CharField(max_length=255)
    index = models.PositiveIntegerField()
    complete = models.BooleanField(default=False)
    def __str__(self):
        return f'{self.user_name} on {self.road} at index {self.index}'
       
