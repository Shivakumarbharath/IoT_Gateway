import RPi.GPIO as GPIO
import pyrebase
from time import sleep
import time
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
 
#set GPIO Pins
GPIO_TRIGGER = 18
GPIO_ECHO = 24
servo=11 
#set GPIO direction (IN / OUT)
GPIO.setup(servo,GPIO.OUT)
GPIO.setup(GPIO_TRIGGER, GPIO.OUT)
GPIO.setup(GPIO_ECHO, GPIO.IN)
 
def distance():
    # set Trigger to HIGH
    GPIO.output(GPIO_TRIGGER, True)
 
    # set Trigger after 0.01ms to LOW
    time.sleep(0.00001)
    GPIO.output(GPIO_TRIGGER, False)

    StartTime = time.time()
    StopTime = time.time()

    # save StartTime
    while GPIO.input(GPIO_ECHO) == 0:
        StartTime = time.time()

    # save time of arrival
    while GPIO.input(GPIO_ECHO) == 1:
        StopTime = time.time()

    # time difference between start and arrival
    TimeElapsed = StopTime - StartTime
    # multiply with the sonic speed (34300 cm/s)
    # and divide by 2, because there and back
    distance = (TimeElapsed * 34300) / 2

    return distance


def actuate(pwm,change):
    pwm.ChangeDutyCycle(change) #change=5,7.5,10


if __name__ == '__main__':
    pwm=GPIO.PWM(11,50)
    pwm.start(5)
    try:
        while True:
            #dist = distance()
            #print ("Measured Distance = %.1f cm" % dist)
            database = firebase.database()
            print(database.get().val())
            pi=database.child("raspberrypi")
            manual=pi.child("manual").get().val()
 #           print("manual value :" , manual,type(manual))
            if int(manual)==1:
                servo=database.child("raspberrypi").child("servo_on").get().val()
#                print("servo :",servo)
                if int(servo)==1:
                    actuate(pwm,7.5)
                    print("Servo ON")
                else:
                    actuate(pwm,5)
                    print("Servo OFF")
            else:
                dist=distance()
                database.child("raspberrypi").update({"sensor":dist})
                print("Data Uploaded")
        # Reset by pressing CTRL + C
    except Exception as e :
        print(e)
    except KeyboardInterrupt:
        pwm.stop()
        print("Measurement stopped by User")
        GPIO.cleanup()
        #data={"servo_on":0,"sensor":0,"manual":0}
        #database.child("raspberrypi").push(data)
