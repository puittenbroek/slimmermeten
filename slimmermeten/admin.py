from django.contrib import admin
from slimmermeten.models import ElektricityReading, GasReading, PowerConsumption


class PowerConsumptionAdmin(admin.ModelAdmin):
	list_display = ('date', 'power')

class ElektricityReadingAdmin(admin.ModelAdmin):
    list_display = ('date', 'tarief', 't1_reading', 't1_back_reading', 't2_stand', 't2_back_reading', )

admin.site.register(ElektricityReading, ElektricityReadingAdmin)
admin.site.register(GasReading)
admin.site.register(PowerConsumption, PowerConsumptionAdmin)