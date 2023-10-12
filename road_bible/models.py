from django.db import models

class RoadProgress(models.Model):
    user_name = models.CharField(max_length=255)  # Add a field for user name
    road = models.CharField(max_length=255)
    index = models.PositiveIntegerField()
    complete = models.BooleanField(default=False)
    def __str__(self):
        return f'{self.user_name} on {self.road} at index {self.index}'
class Settings(models.Model):
    defaultmode = models.CharField(max_length=255, default="randomword")
    color = models.CharField(max_length=255, default='#3876d2')
    translation =models.CharField(max_length=255, default='NIV')
    user_name = models.CharField(max_length=255, default="unknown")  # Add a field for user name
    def __str__(self):
        return f'Mode is: {self.defaultmode} color is: {self.color} translation is {self.translation}'
       
