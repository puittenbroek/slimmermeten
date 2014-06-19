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


def home(request):
    today = datetime.now() - timedelta(hours=24)
    today_min = datetime.combine(today.date(), time.min)
    today_max = datetime.combine(today.date(), time.max)

    # Filter a day?
    consumptions = PowerConsumption.objects.filter(date__range=(today_min, today_max))
    # Unfiltered
    # consumptions = PowerConsumption.objects.all()
    consumptions = consumptions.extra({"hour": "date_trunc('hour', date)"}).values("hour").order_by('hour').annotate(avg_power=Avg("power"))  

    days = []
    cur_date = None
    cur_row = []
    for cons in consumptions:
        hour_date = cons.get('hour')
        power = cons.get('avg_power')
        print hour_date
        if not cur_date:
            # Initial
            cur_date = hour_date.date()
        elif cur_date != hour_date.date():
            # next day
            days.append((cur_date,  cur_row))
            cur_row = []
            cur_date = hour_date.date()
        cur_row.append(int(power))


    days.append((cur_date,  cur_row))
    hours = [u"{0} uur".format(x) for x in range(0,24)]
    print hours
    colors = {}
    for date, values in days:
        colors[date] = get_random_color()[0]

    context = {'days': days, 'hours': hours, 'colors':colors}
    return render(request, 'index.html', context)