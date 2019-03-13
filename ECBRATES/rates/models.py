from django.db import models

# Create your models here.


class Rate(models.Model):
    currency = models.CharField(max_length = 40, null = False)
    cost = models.FloatField(default = None)
    timestamp = models.DateTimeField(auto_now_add=True, blank=True)
