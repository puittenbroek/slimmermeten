""" Default urlconf for slimmermeten """

from django.conf.urls import include, patterns, url
from django.contrib import admin
admin.autodiscover()


def bad(request):
    """ Simulates a server error """
    1 / 0

urlpatterns = patterns('',
    # Power consumption views
    url(r'^consumption/power/all$', 'slimmermeten.views.all_power', name='power_all'),
    url(r'^consumption/power/(?P<dayname>\w+)$', 'slimmermeten.views.power_date', name='power_today'),
    url(r'^consumption/power/(?P<dayname>\w+)/(?P<hour>[\d]{1,2})/$', 'slimmermeten.views.power_date', name='power_today'),
    url(r'^consumption/power/(?P<year>[0-9]{4})/(?P<month>[0-9]{2})/(?P<day>[0-9]{2})/$','slimmermeten.views.power_date',name='power_date'),
    url(r'^consumption/power/(?P<year>[\d]{4})/(?P<month>[\d]{2})/(?P<day>[\d]{2})/(?P<hour>[\d]{1,2})/$','slimmermeten.views.power_date',name='power_date_hour'),
 
    # Electricity Reading Views
    url(r'^reading/electricity/all$', 'slimmermeten.views.all_elektricity', name='elektricity_all'),
    url(r'^reading/electricity/(?P<dayname>\w+)$', 'slimmermeten.views.elektricity_date', name='elektricty_today'),
    url(r'^reading/electricity/(?P<dayname>\w+)/(?P<hour>[\d]{1,2})/$', 'slimmermeten.views.elektricity_date', name='elektricty_today'),
    url(r'^reading/electricity/(?P<year>[0-9]{4})/(?P<month>[0-9]{2})/(?P<day>[0-9]{2})/$','slimmermeten.views.elektricity_date',name='elektricity_date'),
    url(r'^reading/electricity/(?P<year>[\d]{4})/(?P<month>[\d]{2})/(?P<day>[\d]{2})/(?P<hour>[\d]{1,2})/$','slimmermeten.views.elektricity_date',name='elektricity_date_hour'),
 
    # Gas Reading Views
    url(r'^reading/gas/all$', 'slimmermeten.views.all_gas_reading', name='gas_reading_all'),

    # Gas consumption
    # url(r'^consumption/gas/all$', 'slimmermeten.views.all_elektricty', name='power_all'),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^bad/$', bad),
    url(r'', include('base.urls')),
)

