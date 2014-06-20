from django.core.management.base import BaseCommand, CommandError
from slimmermeten.models import PowerConsumption, GasReading, ElektricityReading
import sys
import serial
from datetime import datetime, timedelta
from optparse import make_option
# from django.utils.timezone import utc

class Command(BaseCommand):
    option_list = BaseCommand.option_list + (
        make_option('--regels',
            action='store_true',
            dest='output_rows',
            default=20,
            help='Number of output rows of serialport'),
        )

    @property
    def record_power_consumption(self):
        one_minute_ago = timedelta(seconds=60)
        now = datetime.now()
        record = True   
        last_elek_verbruik = PowerConsumption.objects.all().order_by('-date') 
        if last_elek_verbruik:
            last_date = last_elek_verbruik[0].date
            delta_now = now - last_date
            if delta_now < one_minute_ago:
                record = False
        return record

    @property 
    def record_electricity_reading(self):
        five_minute_ago = timedelta(seconds=300)
        now = datetime.now()
        record = True   
        last_elek_stand = ElektricityReading.objects.all().order_by('-date') 
        if last_elek_stand:
            last_date = last_elek_stand[0].date
            delta_now = now - last_date
            if delta_now < five_minute_ago:
                record = False
        return record

    @property 
    def record_gas_reading(self):
        one_hour_ago =  timedelta(minutes=60)
        now = datetime.now()
        record = True   
        last_gas_stand = GasReading.objects.all().order_by('-date') 
        if last_gas_stand:
            last_date = last_gas_stand[0].date
            delta_now = now - last_date
            if delta_now < one_hour_ago:
                record = False
        return record

    def handle(self, *args, **options):
        # Easy helper
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

        # Timy helpers
        one_minute_ago = timedelta(seconds=60)
        one_hour_ago =  timedelta(minutes=60)
        now = datetime.now()

        # Gas reading
        gas_reading = GasReading()
        gas_reading.date =now

        # Electrcity reading
        electricity_reading = ElektricityReading()
        electricity_reading.date = now

        # Power consumption
        power_consumption = PowerConsumption()
        power_consumption.date = now

        # We usually get 20 lines back from the serial
        # This varies .. as do the identifier probably
        # But for first version, only rows are adjustable.
        p1_teller = 0
        next_is_gas = False

        # Localize
        record_electricity_reading = self.record_electricity_reading
        record_power_consumption = self.record_power_consumption
        record_gas_reading = self.record_gas_reading

        # Early exit.
        if not (record_electricity_reading or record_power_consumption or record_gas_reading):
            printt("Not time to record anything.. exiting")
            ser.close()
            return

        while p1_teller < rows:
            p1_line=''
            #Read 1 line
            p1_line=ser.readline().strip()

            # Dal of piek?
            if p1_line[0:9] == "0-0:96.14" and record_electricity_reading:
                value = int(p1_line[13:-1])
                electricity_reading.tarief = value

            #Reading Low (T1) tarif
            if p1_line[0:9] == "1-0:1.8.1" and record_electricity_reading:
                value = int(p1_line[10:15])
                electricity_reading.t1_reading = value

            #Reading High (T2) tarif
            if p1_line[0:9] == "1-0:1.8.2" and record_electricity_reading:
                value = int(p1_line[10:15])
                electricity_reading.t2_reading = value

            # Reading Low (T1) back to grid
            if p1_line[0:9] == "1-0:2.8.1" and record_electricity_reading:
                value = int(p1_line[10:15])
                electricity_reading.t1_back_reading = value

            # Reading High (T2) back to grid
            if p1_line[0:9] == "1-0:2.8.2" and record_electricity_reading:
                value = int(p1_line[10:15])
                electricity_reading.t2_back_reading = value

            # Current power consumption
            if p1_line[0:9] == "1-0:1.7.0" and record_power_consumption:
                watt_float = float(p1_line[10:17])*1000
                watt_float = int(watt_float)
                power_consumption.power = watt_float

            # Current power delivery back to grid (negative consumption!)
            if p1_line[0:9] == "1-0:2.7.0" and record_power_consumption:
                watt_float = float(p1_line[10:17])*1000
                watt_float = int(watt_float)
                if watt_float > 0:
                    power_consumption.power = watt_float

            # Gasmeter: 0-1:24.3.0. Is followed by the value.
            # We set the flag.
            if p1_line[0:10] == "0-1:24.3.0":
                next_is_gas = True
            elif next_is_gas and record_gas_reading:
                gas_float = float(p1_line[1:10])*1000
                gas_float = int(gas_float)
                next_is_gas = False
                # result['gas_stand'] = gas_float
                gas_reading.reading = gas_float

            # Always up the counter
            p1_teller += 1   

        # Save gas
        if record_gas_reading:
            gas_reading.save()
            printt("- Saved gas reading")

        if record_electricity_reading:
            electricity_reading.save()
            printt("- Saved electricty reading")

        # Save power consumption
        if record_power_consumption:
            power_consumption.save()
            printt("- Saved power consumption")

        ser.close()
        printt("Done")