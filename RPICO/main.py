from machine import Pin, ADC, I2C
import time
import neopixel
from pico_i2c_lcd import I2cLcd
import _thread


#maakt variabelen aan voor neopixel, lcd en de onboard led
led = Pin(25, Pin.OUT)
np = neopixel.NeoPixel(machine.Pin(13), 8)
i2c = I2C(0, sda=Pin(8), scl=Pin(9), freq=400000)
I2C_ADDR = i2c.scan()[0]
lcd = I2cLcd(i2c, I2C_ADDR, 2, 16)

def neopixel_clear():
    #haalt de neopixels leeg
    for i in range(0,8):
        np[i] = (0,0,0)
    np.write()

def neopixel_Loading(value):
    #Maakt een loading bar met neopixel
    neopixel_clear()
    if value == 0:
        for i in range(0, 8):
            np[i] = (255, 0, 0)
            np.write()
            time.sleep(0.5)
    elif value == 1:
        for i in range(0, 8):
            np[i] = (0, 255, 0)
        np.write()
        time.sleep(5)
        neopixel_clear()

def neopixel_status(value):
    #Laat status zien met neopixel met kleur
    neopixel_clear()
    if value == 0:
        #offline
        for i in range(0, 8):
            np[i] = (255, 0, 0)
        np.write()
        time.sleep(5)
        neopixel_clear()

    elif value == 1:
        #online
        for i in range(0, 8):
            np[i] = (0, 255, 0)
        np.write()
        time.sleep(5)
        neopixel_clear()
        
    elif value == 2:
        #busy
        for i in range(0, 8):
            np[i] = (255, 165, 0)
        np.write()
        time.sleep(5)
        neopixel_clear()
    elif value == 3:
        #away
        for i in range(0, 8):
            np[i] = (255, 255, 0)
        np.write()
        time.sleep(5)
        neopixel_clear()


def lcd_display(data):
    #Laat de data zijn op het LCD
    lcd.clear()
    if len(data) <= 16:
        lcd.move_to(0, 0)
        lcd.putstr(data)
        time.sleep(5)
    else:
        #Loopt door de data heen als het meer dan 16 karakters zijn
        for i in range(len(data) - 15):
            lcd.move_to(0, 0)
            lcd.putstr(data[i:i+16])
            time.sleep(0.5)
    
# Knipperen met led om succesvol knipperen te bevestigen
for _ in range(5):
    led(0)
    time.sleep(.1)
    led(1)
    time.sleep(.1)

while True:
    #wacht voor data die naar de PICO wordt gestuurd.
    # als data wordt onvangen check hij als het een commando is of niet en voert hij het uit
    lcd.clear()
    data = input()
    if data == '0':
        neopixel_clear()
        neopixel_Loading(0)
    elif data == '1':
        neopixel_clear()
        neopixel_Loading(1)

    elif "lcd=" in data:
        neopixel_clear()
        lcd.clear()
        data = data.replace("lcd=", "")
        lcd_display(data)
    
    elif 'status=' in data:
        neopixel_clear()
        data = data.replace("status=", "")
        if data == "Offline":
            main_update_thread = _thread.start_new_thread(neopixel_status, (0,))
            lcd_display(data)
        elif data == "Online":
            main_update_thread = _thread.start_new_thread(neopixel_status, (1,))
            lcd_display(data)
        elif data == "Busy":
            main_update_thread = _thread.start_new_thread(neopixel_status, (2,))
            lcd_display(data)
        elif data == "Away":
            main_update_thread = _thread.start_new_thread(neopixel_status, (3,))
            lcd_display(data)
        else:
            neopixel_clear()