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
# Create your views here.

def get_random_color(colors=1):
    returnset = set()
    h,s,v=random()*6,.5,243.2
    i=0
    while len(returnset) < colors:
        h+=3.708;
        returnset.add('#'+'%02x'*3%((v,v-v*s*abs(1-h%2),v-v*s)*3)[5**int(h)/3%3::int(h)%2+1][:3])
        if i%5/4:
            s+=.1
            v-=51.2
        i += 1
    return list(returnset)


def all_power(request):
    # Unfiltered
    consumptions = PowerConsumption.objects.all()
    consumptions = consumptions.extra({"hour": "date_trunc('hour', date)"}).values("hour").order_by('hour').annotate(power=Avg("power"))  

    series = []
    cur_date = None
    cur_row = [0,]*24
    for cons in consumptions:
        hour_date = cons.get('hour')
        power = cons.get('power')
        if not cur_date:
            # Initial
            cur_date = hour_date.date()
        elif cur_date != hour_date.date():
            # next day
            series.append((cur_date,  cur_row))
            cur_row = [0,]*24
            cur_date = hour_date.date()
        cur_row[hour_date.hour] = int(power)


    series.append((cur_date,  cur_row))
    labels = [u"{0:02d}:00".format(x) for x in range(0,24)]

    context = {'series': series, 'labels': labels, 'yaxis_label': 'Power consumption (Watt)', 'graph_title':"Power Consumption", "value_suffix": " Watt"}
    return render(request, 'chart.html', context)

def power_date(request, day=0, month=0, year=0, hour=0, dayname=None):
    if dayname and dayname in ['today','yesterday']:
        thedate = datetime.now()
        name = "Today"
        if dayname =='yesterday':
            thedate = thedate - timedelta(hours=24)
            name = "Yesterday"
    elif dayname:
        raise "No such day"

    if day and month and year:
        thedate = datetime(int(year), int(month), int(day))
        name = "{0}-{1}-{2}".format(day, month, year)
    if hour:
        hour = int(hour)
        name = "{0} {1:02d}:00".format(name, hour)
        today_min = datetime.combine(thedate.date(), time(hour-1,30))
        today_max = datetime.combine(thedate.date(), time(hour,31))
    else:
        today_min = datetime.combine(thedate.date(), time.min)
        today_max = datetime.combine(thedate.date(), time.max)

    consumptions = PowerConsumption.objects.filter(date__range=(today_min, today_max))
    if not hour:
        # When not zoomed on an hour, group per hour
        consumptions = consumptions.extra({"date": "date_trunc('hour', date)"}).values("date").order_by('date').annotate(power=Avg("power"))  
        values = [cons.get('power') for cons in consumptions]
        labels = ["{0:02d}:{1:02d}".format(cons.get('date').hour, cons.get('date').minute) for cons in consumptions]
    else:
        values = [cons.power for cons in consumptions]
        labels = ["{0:02d}:{1:02d}".format(cons.date.hour, cons.date.minute) for cons in consumptions]

    series = [(name,values)]
    context = {'series': series, 'labels': labels, 'yaxis_label': 'Power consumption (Watt)', 'graph_title':"Power Consumption", "value_suffix": " Watt"}
    return render(request, 'chart.html', context)