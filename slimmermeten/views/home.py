from django.shortcuts import render
from django.http import HttpResponse
from django.template import RequestContext, loader
from slimmermeten.models import ElektricityReading, GasReading, PowerConsumption
from django.db.models.aggregates import Count
from django.db.models import Avg
import colorsys
from datetime import datetime, date, time, timedelta
# Create your views here.


def home(request):
    today = datetime.now() - timedelta(hours=24)
    today_min = datetime.combine(today.date(), time.min)
    today_max = datetime.combine(today.date(), time.max)

    # Filter a day?
    # consumptions = PowerConsumption.objects.filter(date__range=(today_min, today_max))
    # Unfiltered
    consumptions = PowerConsumption.objects.all()
    consumptions = consumptions.extra({"hour": "date_trunc('hour', date)"}).values("hour").order_by('hour').annotate(avg_power=Avg("power"))  

    days = {}
    day_order = []
    cur_date = None
    cur_row = [0]*24
    for cons in consumptions:
        hour_date = cons.get('hour')
        hour = hour_date.time().hour
        power = cons.get('avg_power')
        if not cur_date:
            # Initial
            cur_date = hour_date.date()
        elif cur_date != hour_date.date():
            # next day
            days[cur_date] = cur_row
            day_order.append(cur_date)
            cur_row = [0]*24
            cur_date = hour_date.date()
        cur_row[hour] = int(power)


    days[cur_date] = cur_row
    print days
    hours = range(0,24)
    N = 150
    HSV_tuples = [(x*1.0/N, 0.5, 0.5) for x in range(N)]
    RGB_tuples = map(lambda x: (colorsys.hsv_to_rgb(*x) + (0.5, )), HSV_tuples)
    colors = {}
    for ind, day in enumerate(days.keys()):
        colors[day] = RGB_tuples[ind]

    context = {'days': days, 'day_order': day_order, 'hours': hours, 'colors':colors}
    return render(request, 'index.html', context)