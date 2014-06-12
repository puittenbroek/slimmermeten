from django.shortcuts import render
from slimmermeten.models import ElektricityReading, GasReading, PowerConsumption
# Create your views here.


def home(request):

	consumptions = PowerConsumption.objects.all()


	# return ""
