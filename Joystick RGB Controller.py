from gpiozero import Button
from gpiozero import RGBLED
import time
from ADCDevice import *
Z_Pin = 18 # define Z_Pin
button = Button(Z_Pin) # define Button pin according to BCM Numbering
adc = ADCDevice() # Define an ADCDevice class object
a = (250,255)
b = (120,130)
led = RGBLED(red=27, green=23, blue=26, active_high=False)
def setup():
    global adc
    if(adc.detectI2C(0x48)): # Detect the pcf8591.
        adc = PCF8591()
    elif(adc.detectI2C(0x4b)): # Detect the ads7830
        adc = ADS7830()
    else:
        print("No correct I2C address found, \n"
        "Please use command 'i2cdetect -y 1' to check the I2C address! \n"
        "Program Exit. \n");
        exit(-1)
        
def purple():
    led.color = (1,0,1)
def color_off():
    led.color = (0,0,0)
def loop():
    while True:
        global color_off
        val_Z = not button.value # read digital value of axis Z
        val_Y = adc.analogRead(0) # read analog value of axis X and Y
        val_X = adc.analogRead(1)
        print ('value_X: %d ,\tvlue_Y: %d ,\tvalue_Z: %d'%(val_X,val_Y,val_Z))
        time.sleep(0.01)

        if 30 <= val_X <= 135 and val_Y ==0:
            color_off()
            led.red = 1
        elif 230 <= val_X <= 255 and 100 <= val_Y <= 150:
            color_off()
            led.green = 1
        elif 50 <= val_X <= 140 and 220 <= val_Y <= 255 :
            color_off()
            led.blue = 1
        elif val_X == 0 and  67 <= val_Y <= 250:
            color_off()
            led.color = (0,1,1)
        else:
            color_off()
            led.color = (1,0,1)
        
            

def destroy():
    adc.close()
    button.close()
if __name__ == '__main__':
    print ('Program is starting ... ') # Program entrance
    setup()
    try:
        loop()
    except KeyboardInterrupt: # Press ctrl-c to end the program.
        destroy()
        print("Ending program")
        led.red = 0
        led.green = 0
        led.blue = 0
        
