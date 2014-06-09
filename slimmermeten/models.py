from django.db import models

# Create your models here.
class ElektrischStand(models.Model):
	# Kan per 10 seconden, doen per minuut
	date = models.DateTimeField('datum meting')
	# T1 standen (normaal + teruggeleverd)
	t1_stand = models.IntegerField(default=0) #23:00-07:00
	t1_stand_terug = models.IntegerField(default=0) #23:00-07:00

	# T2 standen (normaal + teruggeleverd)
	t2_stand = models.IntegerField(default=0) #07:00-23:00
	t2_stand_terug = models.IntegerField(default=0) #07:00-23:00
	tarief = models.IntegerField(default=0) #0 of 1 (T1 of T2)

class GasStand(models.Model):
	# Gas geeft meestal 1 tick per uur
	date = models.DateTimeField('datum meting')
	stand = models.IntegerField(default=0)

class ElektrischVerbruik(models.Model):
    date = models.DateTimeField('datum meting')
    watt = models.IntegerField(default=0)