import RPi.GPIO as GPIO
import pyrebase
from time import sleep

config = {     
  "apiKey": "AIzaSyAazprjzmWs0sv6RjmvLA0rim-q1m89VeQ ",
  "authDomain": "raspberry-pi-d3db6.firebaseapp.com",
  "databaseURL": "https://raspberry-pi-d3db6-default-rtdb.firebaseio.com/",
  "storageBucket": "raspberry-pi-d3db6.appspot.com"
}

firebase = pyrebase.initialize_app(config) #initialize the communication with the "firebase" servers using the previous config data.
