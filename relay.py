import RPi.GPIO as GPIO 

import time #sleep함수를쓰기위해 



GPIO.setmode(GPIO.BCM)

GPIO.setup(12,GPIO.OUT) #gpio18번 셋업 ->릴레이모듈

GPIO.output(12,False)
time.sleep(3)
GPIO.output(12,True)

GPIO.cleanup()