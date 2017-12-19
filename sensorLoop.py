import RPi.GPIO as GPIO
from gps3.agps3threaded import AGPS3mechanism
from aiocoap import *
import time

context = await Context.create_client_context()

API_ENDPOINT = "192.168.43.8:5000"
f = open("binInfo.txt","r")
companyID = f.readline()
piID = f.readline()
depth = float(f.readline())
binVolume = int(f.readline())
companyID = companyID.rstrip("\n")
piID = piID.rstrip("\n")

f.close()
GPIO.setmode(GPIO.BCM)

TRIG = 20
ECHO = 26

print "Distance Measurement In Progress"

GPIO.setup(TRIG,GPIO.OUT)

GPIO.setup(ECHO,GPIO.IN)
GPIO.output(TRIG, False)


agps_thread = AGPS3mechanism()  # Instantiate AGPS3 Mechanisms
agps_thread.stream_data()
agps_thread.run_thread()

while True:
    print "Waiting For Sensor To Settle"
    time.sleep(2)
    GPIO.output(TRIG, True)
    time.sleep(0.0001)
    GPIO.output(TRIG, False)
    while GPIO.input(ECHO)==0:
        pulse_start = time.time()
    while GPIO.input(ECHO)==1:
        pulse_end = time.time()
    pulse_duration = pulse_end - pulse_start
    distance = pulse_duration * 17150
    distance = round(distance,2)
    volPercentage = 1 - (distance/depth)
    if volPercentage < 0:
        volPercentage = 0
    #Measurements.create(volPercentage)
    prediction = 0
    print distance
    print volPercentage
    if volPercentage > 0.6:
        prediction = 1
    latitude = agps_thread.data_stream.lat
    if latitude != 'n\a':
        print companyID
        tempDict = {'latitude':agps_thread.data_stream.lat,'longitude':agps_thread.data_stream.lon,'percentage_filled':volPercentage,'company_id':companyID,'req_id':piID,'predict_full':prediction,'volume':binVolume}
        print tempDict
        request = Message(code=PUT, payload=payload)
        request.opt.uri_host = API_ENDPOINT
        request.opt.uri_path = "update"
        response = await context.request(request).response
    time.sleep(30)

GPIO.cleanup()
