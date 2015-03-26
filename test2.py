import RPi.GPIO as GPIO
from time import sleep
import time

count = 0
lineNum = 1
GPIO.cleanup()
GPIO.setmode(GPIO.BCM)

pin = 17
buttonPin = 23

GPIO.setup(pin, GPIO.OUT)
GPIO.setup(buttonPin, GPIO.IN)

def letsExit():
	"This exits"
	exit

def writetoFile():
	"This will write the date and log to file"

	global lineNum	
	# Open file for writing
	view = open('testout', 'a')
	parse = open('parseout', 'a')
	view.write(str(lineNum) + ". " + time.strftime("%m/%d/%Y") + " - " + time.strftime("%H:%M:%S") + " - Pressed\n")
	parse.write(str(lineNum) + "," + time.strftime("%m") + "," + time.strftime("%d") + "," + time.strftime("%Y") + "," + time.strftime("%H") + "," + time.strftime("%M") + "," + time.strftime("%S") + "\n")
	view.close()
	parse.close()
	lineNum = lineNum + 1

def parseData():
	"This parses the data"
	secCount = 0
	mostUsed = 0
	mostUsedSec = 0
	lastSecUsed = 0
	parse = open('parseout', 'r')
	for line in parse:
		#for month, day, year, house, minute, second in line.split(",")
		#mylist = line.split(',')
		parcount = 0
		M = [x.strip() for x in line.split(',')]		
		for i in M:
			if parcount == 0:
				Index = i
			if parcount == 1:
				Month = i
			if parcount == 2:
				Day = i
			if parcount == 3:
				Year = i
			if parcount == 4:
				Hour = i	
			if parcount == 5:
				Minute = i
			if parcount == 6:
				Second = i		
			parcount = parcount + 1

		if int(Index) == 1:
			lastSecUsed = Second

		if Second == lastSecUsed:
			secCount = secCount + 1	
		else:
			print "Second: %s at %s times." % (lastSecUsed, secCount)
			if secCount > mostUsed:
				mostUsed = secCount
				mostUsedSec = lastSecUsed	
			lastSecUsed = Second		
			secCount = 1
	print "Second: %s at %s times." % (lastSecUsed, secCount)
	if secCount > mostUsed:
		mostUsed = secCount
		mostUsedSec = lastSecUsed
	print "Most used second: %s at %s times." % (mostUsedSec, mostUsed)

def readButtonPress():
	"Reads the button press"
	while True:
		buttonIn = not GPIO.input(buttonPin)
		if buttonIn == True:
			writetoFile()
			#GPIO.output(pin, False)		
			sleep(0.1)
			#if count > 5:
				#GPIO.output(pin, True)
				#writetoFile()
				#sleep(2)
				#GPIO.output(pin, False)
				#count = 0
		#count = count + 1
		#print(count)
		#sleep(0.9)
		if lineNum > 60:
			break

#readButtonPress()
parseData()
GPIO.cleanup()