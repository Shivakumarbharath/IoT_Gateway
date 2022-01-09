import urllib
import requests
import time
key = "U05L2EMC3XQ8V5WM"  # Put your API Key here
def thermometer():
    while True:
        #Calculate CPU temperature of Raspberry Pi in Degrees C
        temp = int(open('/sys/class/thermal/thermal_zone0/temp').read()) / 1e3 # Get Raspberry Pi CPU temp
        print(temp)
        try:
            conn=urllib.request.urlopen(f'https://api.thingspeak.com/update?api_key={key}&field1={temp}')
            print("\nYour message has successfully been sent!")
            msg=requests.get("https://api.thingspeak.com/channels/1628185/feeds.json?api_key=RLX3HYGE13E2KS9I&results=2")
            msg=msg.json()#['feeds'][-1]['field1']
            print(f"From cloud {msg}")
        except KeyboardInterrupt:
            print("Keyboard Interrupt")
            break
        except:
            print("Connection Failed Trt again\n")
            break
if __name__ == "__main__":
     
   thermometer()
 
