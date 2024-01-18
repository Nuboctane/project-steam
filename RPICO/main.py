from machine import Pin, ADC, I2C
import time
import neopixel
from pico_i2c_lcd import I2cLcd


# Use on-board led
led = Pin(25, Pin.OUT)
np = neopixel.NeoPixel(machine.Pin(13), 8)
i2c = I2C(0, sda=Pin(8), scl=Pin(9), freq=400000)
I2C_ADDR = i2c.scan()[0]
lcd = I2cLcd(i2c, I2C_ADDR, 2, 16)

def neopixel_clear():
    for i in range(0,8):
        np[i] = (0,0,0)
    np.write()

def neopixel_start(value):
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
        
# Blink led to confirm succesful flashing
for _ in range(5):
    led(0)
    time.sleep(.1)
    led(1)
    time.sleep(.1)

# Wait for data from the connection
while True:
    lcd.clear()
    data = input()
    if data == '0':
        neopixel_clear()
        neopixel_start(0)
        print("Turning led on.")
        led(1)
    elif data == '1':
        neopixel_clear()
        neopixel_start(1)
        print("Turning led off.")
        led(0)
    elif "lcd=" in data:
        neopixel_clear()
        lcd.clear()
        data = data.replace("lcd=", "")
        if len(data) <= 16:
            lcd.move_to(0, 0)
            lcd.putstr(data)
        else:
            for i in range(len(data) - 15):
                lcd.move_to(0, 0)
                lcd.putstr(data[i:i+16])
                time.sleep(0.5)