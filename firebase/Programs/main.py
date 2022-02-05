import RPi.GPIO as GPIO # To access the GPIO Pins of Raspberry pi
import pyrebase # APi to communicate with google firebase cloud
from time import sleep # To create a delay
import time
import sys # To access system tools
import Adafruit_DHT #To use the dht sensor
sensor=Adafruit_DHT.DHT11 # specify the type of sensor


# Details To connect to the cloud
config = {     
  "apiKey": "AIzaSyAazprjzmWs0sv6RjmvLA0rim-q1m89VeQ ",
  "authDomain": "raspberry-pi-d3db6.firebaseapp.com",
  "databaseURL": "https://raspberry-pi-d3db6-default-rtdb.firebaseio.com/",
  "storageBucket": "raspberry-pi-d3db6.appspot.com"
}

#initialize the communication with the "firebase" servers using the previous config data.
firebase = pyrebase.initialize_app(config)

#Set the mode to use gpio pins
GPIO.setmode(GPIO.BOARD)

temp=4 # board 7 Gpio number 4
relay=8 # board 8

#set GPIO direction as Output
GPIO.setup(relay,GPIO.OUT)

# function to take values from sensor
def sense(pin):
    humidity, temperature = Adafruit_DHT.read_retry(sensor, pin)
    return humidity,temperature

#function to send connect signal to the relay
def relay_on(pin):
    GPIO.output(pin,False)

#function to send disconnect signal to relay
def relay_off(pin):
    GPIO.output(pin,True)

#Print the data on to terminal
def print_database(d):
    manual=d.child("raspberrypi").child("manual").get().val()
    humidity=d.child("raspberrypi").child("humidity").get().val()
    relay=d.child("raspberrypi").child("relay").get().val()
    temperature=d.child("raspberrypi").child("temperature").get().val()
    if manual=="1":
        print("\n\n\n\nMode : Manual")
    else:
        print("\n\n\n\nMode : Automatic") 
    print(f"\nTemperature = {temperature} Humidity = {humidity}")

if __name__ == '__main__':

    try:
        while True:
            # sense
            hum,tem=sense(temp)
            # connect to cloud database
            database = firebase.database()
            # print database to terminal
            #det=database.get().val()
            print_database(database)
            pi=database.child("raspberrypi")
            manual=pi.child("manual").get().val()
            database.child("raspberrypi").update({"temperature":tem,"humidity":hum})
            if int(manual)==1:
                servo=database.child("raspberrypi").child("relay").get().val()
                if int(servo)==1:
                    relay_on(relay)
                    print("Fan is  ON")
                else:
                    relay_off(relay)
                    print("Fan is  OFF")
            else:
                if tem>=30:
                    relay_on(relay)
                    print("\nFan is ON\n")
                else:
                    relay_off(relay)
                    print("\nFan is Off\n")
            print("Data Uploaded Temperature =",tem)

    # Handle Exceptions
    except Exception as e :
        print(e)
    except KeyboardInterrupt:
        print("Server stopped by User")
        GPIO.cleanup()

