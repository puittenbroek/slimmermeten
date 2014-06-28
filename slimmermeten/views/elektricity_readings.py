from django.shortcuts import render
from django.http import HttpResponse
from django.template import RequestContext, loader
from slimmermeten.models import ElektricityReading
from django.db.models.aggregates import Count
from django.db.models import Avg, Min, Max
import colorsys
from datetime import datetime, date, time, timedelta
from random import random
import math


def all_elektricity(request):
    readings = ElektricityReading.objects.all()
    readings = readings.extra({"hour": "date_trunc('hour', date)"}).values("hour","tarief").order_by('hour')\
    .annotate(
        min_t1=Min("t1_reading"),
        max_t1=Max("t1_reading"),
        min_t2=Min("t2_reading"),
        max_t2=Max("t2_reading"))  

    series = []
    cur_date = None
    cur_row = [0,]*24
    prev_value = None
    for reading in readings:
        hour_date = reading.get('hour')
        tarif = reading.get("tarief")
        if tarif == 0:
            tarif = 1
        min_value = reading.get('min_t{}'.format(tarif), 0)
        max_value = reading.get('max_t{}'.format(tarif), 0)
        print "Min: {0} Max: {1}".format(min_value, max_value)
        
        value = max_value-min_value;
        if value <= 0 and prev_value:
            value = prev_value
        elif prev_value: 
            prev_value = value
        if not cur_date:
            # Initial
            cur_date = hour_date.date()
        elif cur_date != hour_date.date():
            # next day
            series.append((cur_date,  cur_row))
            cur_row = [0,]*24
            cur_date = hour_date.date()
        cur_row[hour_date.hour] = value


    series.append((cur_date,  cur_row))
    labels = [u"{0:02d}:00".format(x) for x in range(0,24)]

    context = {'series': series, 
                'labels': labels, 
                'yaxis_label': 'Reading (kWH)', 
                'graph_title':"Elektricity Reading",
                "value_suffix": " kWH"}
    return render(request, 'chart.html', context)


def elektricity_date(request, day=0, month=0, year=0, hour=0, dayname=None):
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

    readings = ElektricityReading.objects.filter(date__range=(today_min, today_max))
    if not hour:
        # When not zoomed on an hour, group per hour
        readings = readings.extra({"date": "date_trunc('hour', date)"}).values("date","tarief").order_by('date').annotate(t1_reading=Avg("t1_reading"),t2_reading=Avg("t2_reading")) 
        values = []
        for reading in readings:
            tarif = reading.get("tarief")
            if tarif == 0:
                tarif = 1
            if tarif == 1:
                continue
            value = reading.get('t{}_reading'.format(tarif), 0)
            values.append(value)
        labels = ["{0:02d}:{1:02d}".format(reading.get('date').hour, reading.get('date').minute) for reading in readings if reading.get("tarief") > 1]
    else:
        values = []
        for reading in readings:
            tarif = reading.get("tarief")
            if tarif == 0:
                tarif = 1
            value = getattr(reading,'t{}_reading'.format(tarif), 0)
            values.append(value)
        labels = ["{0:02d}:{1:02d}".format(reading.date.hour, reading.date.minute) for reading in readings]

    series = [(name,values)]
    context = {'series': series, 
                'labels': labels, 
                'yaxis_label': 'Reading (kWH)', 
                'graph_title':"Elektricity Reading",
                "value_suffix": " kWH"}
    return render(request, 'chart.html', context)