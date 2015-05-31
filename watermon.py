import RPi.GPIO as GPIO
from time import sleep
import time
import datetime


count = 0
lineNum = 1
lastTime = 10
flowSessionCount = 0
GPIO.cleanup()
GPIO.setmode(GPIO.BCM)

pin = 17
buttonPin = 23
lastTime = 1000


GPIO.setup(pin, GPIO.OUT)
GPIO.setup(buttonPin, GPIO.IN)

def letsExit():
	"This exits"
	exit

def writetoFile():
	"This will write the date and log to file"
	
	second = int(time.strftime("%S"))
	global lineNum	
	global lastTime

	# Open file for writing
	view = open('testout', 'a')
	parse = open('parseout', 'a')
 	
	if((second - lastTime) > 2 or (second - lastTime) < -2):
		lastTime = 1000
	if(lastTime > 60):
		parse.write(str("1,"))
	else:
		parse.write(str("0,"))
	view.write(str(lineNum) + ". " + time.strftime("%m/%d/%Y") + " - " + time.strftime("%H:%M:%S") + " - Pressed\n")
	parse.write(str(lineNum) + "," + time.strftime("%m") + "," + time.strftime("%d") + "," + time.strftime("%Y") + "," + time.strftime("%H") + "," + time.strftime("%M") + "," + time.strftime("%S") + "," + datetime.date.today().strftime("%w") + "\n")
	view.close()
	parse.close()
	lineNum = lineNum + 1
	lastTime = second

def parseData():
	"This parses the data"

	global lastTime
	lastTime = 10
	trackWeekday = 10
	global flowSessionCount
	startFlowFlag = 0
	secCount = 0
	Second = 0
	mostUsed = 0
	mostUsedSec = 0
	lastSecUsed = 0
	parse = open('parseout', 'r')
	parsedData = open('parsedData', 'a')
	for line in parse:
		Hour = 0
		#for month, day, year, house, minute, second in line.split(",")
		#mylist = line.split(',')
		parcount = 0
		M = [x.strip() for x in line.split(',')]		
		for i in M:
			if parcount == 0:
				startFlowFlag = i
			if parcount == 1:
				Index = i
			if parcount == 2:
				Month = i
			if parcount == 3:
				Day = i
			if parcount == 4:
				Year = i
			if parcount == 5:
				Hour = i	
			if parcount == 6:
				Minute = i
			if parcount == 7:
				Second = i
			if parcount == 8:
				DayOfWeek = i		
			parcount = parcount + 1

		if int(startFlowFlag) == 1:
			if lastTime == 10:
				parsedData.write(DayOfWeek + "," + Year + "/" + Month + "/" + Day + 
				"," + Hour + ":" + Minute + ":" + Second + ",")
			else:
				parsedData.write(str(lastTime) + "," + str(flowSessionCount) + "\n")
				
				parsedData.write(DayOfWeek + "," + Year + "/" + Month + "/" + Day + 
				"," + Hour + ":" + Minute + ":" + Second + ",")
			flowSessionCount = 0
		
		lastTime = str(Hour) + ":" + str(Minute) + ":" + str(Second)
		flowSessionCount += 1 	

		#if int(Index) == 1:
			#lastSecUsed = Second

		#if Second == lastSecUsed:
			#secCount = secCount + 1	
		#else:
			#print "Second: %s at %s times." % (lastSecUsed, secCount)
			#if secCount > mostUsed:
				#mostUsed = secCount
				#mostUsedSec = lastSecUsed	
			#lastSecUsed = Second		
			#secCount = 1

	#print "Second: %s at %s times." % (lastSecUsed, secCount)
	#if secCount > mostUsed:
		#mostUsed = secCount
		#mostUsedSec = lastSecUsed
	#print "Most used second: %s at %s times." % (mostUsedSec, mostUsed)

	parsedData.write(str(lastTime) + "," + str(flowSessionCount) + "\n")

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
