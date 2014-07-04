#connect arduino tx to P9_26 via a voltage divider (one 10K resistor in series + one to ground)
#also install pyserial with sudo apt-get install pyserial

import Adafruit_BBIO.UART as UART
import serial
import time

###serial in port 1 is "P9_26"

UART.setup("UART1")
ser= serial.Serial(port= "/dev/ttyO1", baudrate= 57600)
if ser.isOpen():
	print "Serial is open!" #debug
	print dir(ser) #debug
	while True:
		print ser.readline()
		time.sleep(0.01) #optional
