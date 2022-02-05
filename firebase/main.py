import RPi.GPIO as GPIO
import pyrebase
from time import sleep
import time
import sys
import Adafruit_DHT
sensor=Adafruit_DHT.DHT11



config = {     
  "apiKey": "AIzaSyAazprjzmWs0sv6RjmvLA0rim-q1m89VeQ ",
  "authDomain": "raspberry-pi-d3db6.firebaseapp.com",
  "databaseURL": "https://raspberry-pi-d3db6-default-rtdb.firebaseio.com/",
  "storageBucket": "raspberry-pi-d3db6.appspot.com"
}

firebase = pyrebase.initialize_app(config) #initialize the communication with the "firebase" servers using the previous config data.

#database = firebase.database()
#RGBControlBucket = database.child("RGBControl")
#powerState = RGBControlBucket.child("powerState").get().val()


GPIO.setmode(GPIO.BOARD)
 
temp=4 # board 7
relay=8 # board 8
#set GPIO direction (IN / OUT)
GPIO.setup(relay,GPIO.OUT)
 
def sense(pin):
    humidity, temperature = Adafruit_DHT.read_retry(sensor, pin)
    return humidity,temperature

def relay_on(pin):
    GPIO.output(pin,False)
def relay_off(pin):
    GPIO.output(pin,True)


if __name__ == '__main__':

    try:
        while True:
            hum,tem=sense(temp)
            database = firebase.database()
            print(database.get().val())
            pi=database.child("raspberrypi")
            manual=pi.child("manual").get().val()
            database.child("raspberrypi").update({"temperature":tem,"humidity":hum})
            if int(manual)==1:
                servo=database.child("raspberrypi").child("relay").get().val()
                if int(servo)==1:
                    relay_on(relay)
                    print("Fan ON")
                else:
                    relay_off(relay)
                    print("Fan OFF")
            else:
                if tem>=30:
                    relay_on(relay)
                else:
                    relay_off(relay)
            print("Data Uploaded Temperature =",tem)

    except Exception as e :
        print(e)
    except KeyboardInterrupt:
        print("Server stopped by User")
        GPIO.cleanup()
        
