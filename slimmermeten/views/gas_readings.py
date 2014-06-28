from django.shortcuts import render
from django.http import HttpResponse
from django.template import RequestContext, loader
from slimmermeten.models import ElektricityReading, GasReading, PowerConsumption
from django.db.models.aggregates import Count
from django.db.models import Avg
import colorsys
from datetime import datetime, date, time, timedelta
from random import random
import math


def all_gas_reading(request):
    pass

def gas_reading_date(request):
    pass