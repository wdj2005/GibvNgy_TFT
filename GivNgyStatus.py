from ST7735 import TFT
from terminalfont import terminalfont
from machine import SPI,Pin,RTC
import time
import math
import network
import urequests
import ntptime
import secrets

# Initialize TFT SPI interface
spi = SPI(1, baudrate=20000000, polarity=0, phase=0,
          sck=Pin(10), mosi=Pin(11), miso=None)
tft=TFT(spi,16,17,18)
tft.initr()
tft.rgb(False)
tft.fill(TFT.BLACK)

# Connect to WLAN
wlan = network.WLAN(network.STA_IF)
wlan.active(True)
wlan.connect(secrets.SSID, secrets.PASSWORD)
while not wlan.isconnected():
    pass
print('Connected to WLAN')

time.sleep(3)

#Set the time with NTP
rtc = RTC()
ntptime.settime()
print(rtc.datetime())

while True:

    # Make GivEnergy API call to get Inverter data
    url = "https://api.givenergy.cloud/v1/inverter/"+secrets.INVERTER+"/system-data/latest"
    headers = {
      'Authorization': 'Bearer '+ secrets.API_KEY,
      'Content-Type': 'application/json',
      'Accept': 'application/json'
    }
    print ('Making API call..')
    response = urequests.request('GET',url,headers=headers)
    data = response.json()
    batt_lvl = data['data']['battery']['percent']
    print(batt_lvl)
    now=rtc.datetime() # get date and time
    print(now)
    print("{:02d}-{:02d}-{:04d} {:02d}:{:02d}:{:02d}".format(now[2],now[1],now[0],now[4],now[5],now[6]))
   
    

    tft.fill(TFT.BLACK) #'clear' the screen before updates
    tft.text((0, 0), secrets.INVERTER, TFT.BLUE, terminalfont, 2, nowrap=True)
    tft.text((0, 20), "BATTERY", TFT.GREEN, terminalfont, 2, nowrap=True)
    tft.text((0, 40), str(batt_lvl)+"%", TFT.PURPLE, terminalfont, 4)
    tft.text((0,100), str(now[4])+":"+str(now[5]), TFT.YELLOW, terminalfont, 2, nowrap=True)
    time.sleep(60)
 

