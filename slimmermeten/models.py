from django.db import models


class ElektricityReading(models.Model):
	# Gives a tick per 10 seconds? We measure per minute
	date = models.DateTimeField('date of measurement')
	# T1 standen (normal + back to grid)
	t1_reading = models.IntegerField(default=0) #23:00-07:00
	t1_back_reading = models.IntegerField(default=0) #23:00-07:00

	# T2 standen (normal + back to grid)
	t2_reading = models.IntegerField(default=0) #07:00-23:00
	t2_back_reading = models.IntegerField(default=0) #07:00-23:00

	tarief = models.IntegerField(default=0) #0 of 1 (T1 of T2)

class GasReading(models.Model):
	# Gas usually gives 1 ticker per hour
	date = models.DateTimeField('date of measurement')
	reading = models.IntegerField(default=0)

class PowerConsumption(models.Model):
    date = models.DateTimeField('date of measurement')
    power = models.IntegerField(default=0)