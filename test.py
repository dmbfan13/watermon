import RPi.GPIO as GPIO
from time import sleep
import time

def letsExit():
	"This exits"
	exit

def writetoFile():
	"This will write the date and log to file"
	# Open file for writing
	f = open('testout', 'a')
	f.write(time.strftime("%m/%d/%Y") + " - " + time.strftime("%H:%M:%S") + "\n")
	f.close()

GPIO.cleanup()
GPIO.setmode(GPIO.BCM)

count = 0
pin = 17
buttonPin = 23

GPIO.setup(pin, GPIO.OUT)
GPIO.setup(buttonPin, GPIO.IN)

while True:
	buttonIn = not GPIO.input(buttonPin)
	if buttonIn == True:
		#GPIO.output(pin, False)
		count = count + 1
		print(count)
		sleep(0.2)
		if count > 5:
			GPIO.output(pin, True)
			writetoFile()
			sleep(2)
			GPIO.output(pin, False)
			count = 0

GPIO.cleanup()