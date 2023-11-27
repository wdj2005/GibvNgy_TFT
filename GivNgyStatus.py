from ST7735 import TFT
from terminalfont import terminalfont
from machine import SPI,Pin
import time
import math
import network
import urequests
import secrets

# Initialize TFT SPI interface
spi = SPI(1, baudrate=20000000, polarity=0, phase=0,
          sck=Pin(10), mosi=Pin(11), miso=None)
tft=TFT(spi,16,17,18)
tft.initr()
tft.rgb(True)
tft.fill(TFT.BLACK)

# Connect to WLAN
wlan = network.WLAN(network.STA_IF)
wlan.active(True)
wlan.connect(secrets.SSID, secrets.PASSWORD)
while not wlan.isconnected():
    pass
print('Connected to WLAN')

time.sleep(3)

while True:

    # Make GivEnergy API call to get Inverter data
    url = "https://api.givenergy.cloud/v1/inverter/"+secrets.INVERTER+"/system-data/latest"
    headers = {
      'Authorization': 'Bearer '+ secrets.API_KEY,
      'Content-Type': 'application/json',
      'Accept': 'application/json'
    }

    response = urequests.request('GET',url,headers=headers)
    data = response.json()
    batt_lvl = data['data']['battery']['percent']
    print(batt_lvl)

    tft.fill(TFT.BLACK) #'clear' the screen before updates
    tft.text((0, 0), "BATTERY", TFT.GREEN, terminalfont, 2, nowrap=True)
    tft.text((0, 20), str(batt_lvl)+"%", TFT.PURPLE, terminalfont, 4)
    time.sleep(60)
 

