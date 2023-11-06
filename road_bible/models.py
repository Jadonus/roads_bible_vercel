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
    translation = models.CharField(max_length=255, default='NLT')
    # Add a field for user name
    user_name = models.CharField(max_length=255, default="unknown")

    def __str__(self):
        return f'Mode is: {self.defaultmode} color is: {self.color} translation is {self.translation}'


class CustomRoads(models.Model):
    verses = models.JSONField()
    title = models.CharField(max_length=255)
    creator = models.CharField(max_length=255)

    def __str__(self):
        return f'Verses are {self.verses}  title is {self.title}creator is{self.creator} '


class Favorites(models.Model):
    title = models.CharField(max_length=255)
    index = models.PositiveIntegerField(default=0)
    user_name = models.CharField(max_length=255)
    road = models.BooleanField(default=True)
    verse= models.CharField(max_length=255, default="N/A")

    def __str__(self):
        return f'Title is {self.title}  index is {self.index}creator is{self.user_name} road is {self.road}'
