from django.core.management.base import BaseCommand, CommandError
from slimmermeten.models import ElektrischVerbruik, GasStand, ElektrischStand
import sys
import serial
from datetime import datetime, timedelta
from optparse import make_option

class Command(BaseCommand):
    option_list = BaseCommand.option_list + (
        make_option('--regels',
            action='store_true',
            dest='output_rows',
            default=20,
            help='Number of output rows of serialport'),
        )

    @property
    def record_elek_verbruik(self):
        one_minute_ago = timedelta(seconds=60)
        now = datetime.now()   
        record = True   
        last_elek_verbruik = ElektrischVerbruik.objects.all().order_by('-date') 
        if last_elek_verbruik:
            last_date = last_elek_verbruik[0].date
            delta_now = now - last_date
            if delta_now < one_minute_ago:
                record = False
        return True

    @property 
    def record_elek_stand(self):
        one_minute_ago = timedelta(seconds=60)
        now = datetime.now()   
        record = True   
        last_elek_stand = ElektrischStand.objects.all().order_by('-date') 
        if last_elek_stand:
            last_date = last_elek_stand[0].date
            delta_now = now - last_date
            if delta_now < one_minute_ago:
                record = False
        return True

    @property 
    def record_gas_stand(self):
        one_hour_ago =  timedelta(minutes=60)
        now = datetime.now()   
        record = True   
        last_gas_stand = GasStand.objects.all().order_by('-date') 
        if last_gas_stand:
            last_date = last_gas_stand[0].date
            delta_now = now - last_date
            if delta_now < one_hour_ago:
                record = False
        return True

    def handle(self, *args, **options):
        printt = self.stdout.write
        #Set COM port config
        ser = serial.Serial()
        ser.baudrate = 9600
        ser.bytesize=serial.SEVENBITS
        ser.parity=serial.PARITY_EVEN
        ser.stopbits=serial.STOPBITS_ONE
        ser.xonxoff=0
        ser.rtscts=0
        ser.timeout=10
        ser.port="/dev/ttyUSB0"

        # Open the port
        ser.open()

        # Rows
        rows = int(options['output_rows'])
        one_minute_ago = timedelta(seconds=60)
        one_hour_ago =  timedelta(minutes=60)
        now = datetime.now()

        printt("Gasstand: %s" % self.record_gas_stand)
        printt("Elekstand: %s " % self.record_elek_stand)
        printt("Elekverbruik: %s " % self.record_elek_verbruik)


        p1_teller=0
        while p1_teller < rows:
            p1_line=''
            #Read 1 line
            p1_line=ser.readline().strip()

            # Dal of piek?
            if p1_line[0:9] == "0-0:96.14":
                waarde = int(p1_line[13:-1])
                result['elektriciteit_tarief'] = waarde and 'dal' or 'piek'
            #Meterstand Daltarief
            elif p1_line[0:9] == "1-0:1.8.1":
                result['elektriciteit_dal_stand'] = int(p1_line[10:15])

            #Meterstand Piektarief
            elif p1_line[0:9] == "1-0:1.8.2":
                result['elektriciteit_piek_stand'] = int(p1_line[10:15])

            # Daltarief, teruggeleverd vermogen 1-0:2.8.1
            elif p1_line[0:9] == "1-0:2.8.1":
                result['elektriciteit_dal_terug'] = int(p1_line[10:15])

            # Piek tarief, teruggeleverd vermogen 1-0:2.8.2
            elif p1_line[0:9] == "1-0:2.8.2":
                result['elektriciteit_piek_terug'] = int(p1_line[10:15])

            # Huidige elektriciteitafname: 1-0:1.7.0
            elif p1_line[0:9] == "1-0:1.7.0":
                watt_float = float(p1_line[10:17])*1000
                watt_float = int(watt_float)
                result['elektriciteit_huidig'] = watt_float

            # Huidig teruggeleverd vermogen: 1-0:1.7.0
            elif p1_line[0:9] == "1-0:2.7.0":
                watt_float = float(p1_line[10:17])*1000
                watt_float = int(watt_float)
                result['elektriciteit_huidig_terug'] = watt_float

            # Gasmeter: 0-1:24.3.0
            elif p1_line[0:10] == "0-1:24.3.0":
                next_is_gas = True
            elif next_is_gas:
                gas_float = float(p1_line[1:10])*1000
                gas_float = int(gas_float)
                next_is_gas = False
                result['gas_stand'] = gas_float
            p1_teller += 1   
        # poll.opened = False
        # poll.save()
        # printt('last_elek_verbruik: "%s"' % last_elek_verbruik)
        # printt('last_elek_stand: "%s"' % last_elek_stand)
        # printt('last_gas_stand: "%s"' % last_gas_stand)