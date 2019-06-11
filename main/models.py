from django.db import models

# Create your models here.


class Branch(models.Model):
    # Код подразделения,Субъект федерации,Город,Улица,Дом,Широта,Долгота
    code = models.IntegerField(primary_key=True)
    region = models.CharField(max_length=50)
    city = models.CharField(max_length=100)
    street = models.CharField(max_length=100)
    building = models.CharField(max_length=20)
    latitude = models.FloatField()
    longitude = models.FloatField()
    is_deleted = models.BooleanField(default=0, null=True, blank=True)


class City(models.Model):
    title = models.CharField(max_length=50, primary_key=True)
    density = models.FloatField()
    pop = models.FloatField()
