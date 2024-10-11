from django.db import models

class Table(models.Model):
    number = models.IntegerField(unique=True)
    seats = models.IntegerField()
    x_position = models.FloatField()
    y_position = models.FloatField()
