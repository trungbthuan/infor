from django.db import models

class Students(models.Model):
    id = models.IntegerField(primary_key=True, auto_created=True)
    full_name = models.CharField(max_length=225)
    birthday = models.DateField()
    sex = models.CharField(max_length=10)
    class_name = models.CharField(max_length=10)
    average = models.FloatField()
    morality = models.CharField(max_length=15)
    performance = models.CharField(max_length=15)

class Profiles(models.Model):
    id = models.IntegerField(primary_key=True, auto_created=True)
    full_name = models.CharField(max_length=225)
    birthday = models.DateField()
    sex = models.CharField(max_length=10)
    birth_place = models.CharField(max_length=225)
    nation = models.CharField(max_length=30)
    recruitment_day = models.DateField()
    job_title = models.CharField(max_length=225)
    department = models.CharField(max_length=225)