import os
os.system('cls' if os.name == 'nt' else 'clear')
from rich.console import Console


con=Console()
with con.status("Initialising ...",spinner="aesthetic"):
    con.log("Importing Libraries...")
    import RPi.GPIO as GPIO # To access the GPIO Pins of Raspberry pi
    import pyrebase # APi to communicate with google firebase cloud
    from time import sleep # To create a delay
    import time
    import sys # To access system tools
    import Adafruit_DHT #To use the dht sensor
    sensor=Adafruit_DHT.DHT11 # specify the type of sensor
    from rich import print as rprint
    from rich.panel import Panel
    from rich.live import Live
    import sys
    con.log("Importing [green]Sucessfull...")


# Details To connect to the cloud
    config = {     
      "apiKey": "AIzaSyAazprjzmWs0sv6RjmvLA0rim-q1m89VeQ ",
      "authDomain": "raspberry-pi-d3db6.firebaseapp.com",
      "databaseURL": "https://raspberry-pi-d3db6-default-rtdb.firebaseio.com/",
      "storageBucket": "raspberry-pi-d3db6.appspot.com"
    }
    con.log("Configuring Database [green]Sucessfull...")

#initialize the communication with the "firebase" servers using the previous config data.
    firebase = pyrebase.initialize_app(config)
    con.log("Connection with Firebase [green]Successfull...")
#Set the mode to use gpio pins
    GPIO.setmode(GPIO.BOARD)
    con.log("Setting up Raspberry pi [green]Successfull...")

    temp=4 # board 7 Gpio number 4
    relay=8 # board 8

#set GPIO direction as Output
    GPIO.setup(relay,GPIO.OUT)
    con.log("[green bold]Device Ready for Operation...")
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
        mode="Manual"
        #print("\n\n\n\nMode : Manual")
    else:
        mode="Automatic"
        #print("\n\n\n\nMode : Automatic") 
    #print(f"\nTemperature = {temperature} Humidity = {humidity}")
    txt=f"""
       Mode :{mode}\n\n
Temperature : {temperature}\n\n
Humidity    : {humidity}\n\n
        """
    return txt


def main(c):
    # sense
    hum,tem=sense(temp)
    # connect to cloud database
    database = firebase.database()
    # print database to terminal
    #det=database.get().val()
    etxt=print_database(database)
    pi=database.child("raspberrypi")
    manual=pi.child("manual").get().val()
    database.child("raspberrypi").update({"temperature":tem,"humidity":hum})
    if int(manual)==1:
        servo=database.child("raspberrypi").child("relay").get().val()
        if int(servo)==1:
            relay_on(relay)
            #print("Fan is  ON")
            etxt+="Fan : ON\n\n"
        else:
            relay_off(relay)
            #print("Fan is  OFF")
            etxt+="Fan : OFF\n\n"
    else:
        if tem>=30:
            relay_on(relay)
            #print("\nFan is ON\n")
            etxt+="Fan : ON\n\n"
        else:
            relay_off(relay)
            #print("\nFan is Off\n")
            etxt+="Fan : OFF\n\n"
    #print("Data Uploaded Temperature =",tem)
    etxt+=f"Data Updated and Uploaded\n\nTemparature : {tem}\n\n   Humidity : {hum}"
    if c==1:
        os.system('cls' if os.name == 'nt' else 'clear')
    
    rprint(Panel(etxt,title="Sensor Values",expand=False,highlight=True,padding=[3,3]))
    return etxt
    #con.rule("End")
    


if __name__ == '__main__':

    try:
        while True:
            etxt=main(1)
                
    # Handle Exceptions
    except Exception as e :
        print(e)
        GPIO.cleanup()
    except KeyboardInterrupt:
        os.system('cls' if os.name == 'nt' else 'clear')
        con.log("Importing Libraries...")
        con.log("Importing [green]Sucessfull...")
        con.log("Configuring Database [green]Sucessfull...")
        con.log("Connection with Firebase [green]Successfull...")
        con.log("Setting up Raspberry pi [green]Successfull...")
        con.log("Device Ready for Operation...")
        rprint(Panel(etxt,title="Sensor Values",expand=False,highlight=True,padding=[1,1]))
        
        GPIO.cleanup()
        con.rule("[red bold]Server stopped by User")
        

