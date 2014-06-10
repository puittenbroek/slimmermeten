#
# DSMR P1 uitlezer
# (c) 10-2012 - GJ - gratis te kopieren en te plakken

versie = "1.0"
import sys
import serial
from datetime import datetime


################################################################################################################################################
#Main program
################################################################################################################################################
print ("DSMR P1 uitlezer",  versie)
print ("Control-C om te stoppen")

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

#Open COM port
try:
    ser.open()
except:
    sys.exit ("Fout bij het openen van %s. Programma afgebroken."  % ser.name)      


#Initialize
# stack is mijn list met de 20 regeltjes.
p1_teller=0


result = {}
result['date'] = datetime.now()

next_is_gas = False
while p1_teller < 20:
    p1_line=''
#Read 1 line
    try:
        p1_raw = ser.readline()
    except:
        sys.exit ("Seriele poort %s kan niet gelezen worden. Programma afgebroken." % ser.name )      
    p1_str=str(p1_raw)
    p1_line=p1_str.strip()

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
 
#Close port and show status
try:
    ser.close()
except:
    sys.exit ("Oops %s. Programma afgebroken." % ser.name )     

from pprint import pprint
pprint(result)

 
