#
# DSMR P1 uitlezer
# (c) 02-2022 2016 - GJ - gratis te kopieren en te plakken

versie = "2.0 python3"
import sys
import serial

################
#Error display #
################
def show_error():
    ft = sys.exc_info()[0]
    fv = sys.exc_info()[1]
    print("Fout type: %s" % ft )
    print("Fout waarde: %s" % fv )
    return


################################################################################################################################################
#Main program
################################################################################################################################################
print ("DSMR 5.0 P1 uitlezer",  versie)
print ("Control-C om te stoppen")

#Set COM port config
ser = serial.Serial()
ser.baudrate = 115200
ser.bytesize=serial.EIGHTBITS
ser.parity=serial.PARITY_NONE
ser.stopbits=serial.STOPBITS_ONE
ser.xonxoff=0
ser.rtscts=0
ser.timeout=20
ser.port="/dev/ttyUSB0"

#Open COM port
try:
    ser.open()
except:
    sys.exit ("Fout bij het openen van %s. Programma afgebroken."  % ser.name)      


#Initialize
# stack is mijn list met de 26 regeltjes.
p1_teller=0
stack=[]

while p1_teller < 26:
    p1_line=''
#Read 1 line
    try:
        p1_raw = ser.readline()
    except:
        sys.exit ("Seriele poort %s kan niet gelezen worden. Programma afgebroken." % ser.name )      
    p1_str=str(p1_raw)
    #p1_str=str(p1_raw, "utf-8")
    p1_line=p1_str.strip()
    stack.append(p1_line)
# als je alles wil zien moet je de volgende line uncommenten
    #print (p1_line)
    p1_teller = p1_teller +1

#Initialize
# stack_teller is mijn tellertje voor de 26 weer door te lopen. Waarschijnlijk mag ik die p1_teller ook gebruiken
stack_teller=0
meter=0
fieldcounter = 0

while stack_teller < 26:
   # this is the part of the string where the proper label is indicated
   labelfield=stack[stack_teller][2:11]
   # this is the part which contains de value in Kwh
   valuefield=stack[stack_teller][12:18]
   if labelfield == "1-0:1.8.1":
   # looks like this b'1-0:1.8.1(011215.804*kWh)\r\n'
     print("daldag      ", valuefield)
     meter = meter +  int(float(valuefield))
     fieldcounter +=1
   elif labelfield == "1-0:1.8.2":
     print("piekdag     ", valuefield)
     meter = meter + int(float(valuefield))
     fieldcounter +=1
#    print "meter totaal   ", meter
# Daltarief, teruggeleverd vermogen 1-0:2.8.1
   elif labelfield == "1-0:2.8.1":
     print("dalterug    ", valuefield)
     meter = meter - int(float(valuefield))
     print("meter totaal   ", meter)
     fieldcounter +=1
# Piek tarief, teruggeleverd vermogen 1-0:2.8.2
   elif labelfield == "1-0:2.8.2":
     print("piekterug   ", valuefield)
     meter = meter - int(float(valuefield))
     fieldcounter +=1
# mijn verbruik was op 17-10-2014 1751 kWh teveel teruggeleverd. Nieuw jaar dus opnieuw gaan rekenen
# volgende rij dus uncommenten om een berekening van vorige jaren eraf te tellen.
# meter = meter + 1751
# Nieuwe EMSR 5.0 meter per 01-11-2017, dus opnieuw beginnen met tellen.
     print("meter totaal  ", meter, " (afgenomen/teruggeleverd van het net vanaf 01-11-2017)")
# Huidige stroomafname: 1-0:1.7.0
   elif labelfield == "1-0:1.7.0":
     print("Afgenomen vermogen      ", int(float(valuefield)*1000), " W")
     fieldcounter +=1
# Huidig teruggeleverd vermogen: 1-0:1.7.0
   elif labelfield == "1-0:2.7.0":
     print("Teruggeleverd vermogen  ", int(float(valuefield)*1000), " W")
     fieldcounter +=1
# Gasmeter: 0-1:24.2.1
#  elif stack[stack_teller][0:10] == "0-1:24.2.1":

# Gasmeter: 0-1:24.2.1
#  elif stack[stack_teller][0:10] == "0-1:24.2.1":

# Helaas, 26-09-2016, ik krijg het gas niet aan de gang.
#        print("Gas                     ", int(float(stack[stack_teller][26:35])*1000), " dm3")

   else:
      pass
   stack_teller = stack_teller +1

print("Total nr of fields is {0}. This should be 6 so something went wrong".format(fieldcounter))
#Debug
#print (stack, "\n")
    
#Close port and show status
try:
    ser.close()
except:
    sys.exit ("Oops %s. Programma afgebroken." % ser.name )      
