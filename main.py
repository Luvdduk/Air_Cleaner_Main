from gpiozero import Button, LED, RGBLED, OutputDevice, DigitalOutputDevice
from colorzero import Color
from signal import pause
from threading import Thread
import time
import serial
from PMS7003 import PMS7003
import RPi.GPIO as GPIO

import lcd_i2c as lcd



power_state=0

powersw = Button(26)

#먼지센서 오브젝트
dustlib = PMS7003()

Speed = 9600
SERIAL_PORT = '/dev/ttyUSB0'

# led r:16 g:20 b:21
# 릴레이: 19
fan = OutputDevice(19)
# fan = LED(19)

led = RGBLED(16, 20, 21)

# led_r = LED(16)
# led_g = LED(20)
# led_b = LED(21)


lcd.lcd_init()



# 파워 모드변경
def power():
    global power_state
    powersw.when_pressed = powerctrl
    pause()
# 꺼짐: 0, 켜짐: 1, 자동: 2
def powerctrl():
    global power_state
    if power_state == 0:
        power_state = 1
        print("전원켬")
        # fan.on()
        return
    if power_state == 1:
        power_state = 2
        print("자동모드로 변경")
        # if pm25 >=30 :
        #     fan.on()
        # else:
        #     fan.off()
        return
    if power_state == 2:
        power_state = 0
        print("전원끔")
        # fan.off()
        return

        




#메인루프에 추가

# def update_Dust():
#     while True:
#         #serial setting
#         ser = serial.Serial(SERIAL_PORT, Speed, timeout = 1)
#         buffer = ser.read(1024)

#         if(dustlib.protocol_chk(buffer)):
#             data = dustlib.unpack_data(buffer)

#             pm1 = data[dustlib.DUST_PM1_0_ATM]
#             pm25 = data[dustlib.DUST_PM2_5_ATM]
#             pm10 = data[dustlib.DUST_PM10_0_ATM]
            
#             print ("PMS 7003 dust data")
#             # print ("PM 1.0 : %s" % (data[dustlib.DUST_PM1_0_ATM]))
#             # print ("PM 2.5 : %s" % (data[dustlib.DUST_PM2_5_ATM]))
#             # print ("PM 10.0 : %s" % (data[dustlib.DUST_PM10_0_ATM]))
#             print ("PM 1.0 : %s" % (pm1))
#             print ("PM 2.5 : %s" % (pm25))
#             print ("PM 10.0 : %s" % (pm10))

#         else:
#             print ("data read Err")
#         time.sleep(1)

def display_dust(duststate1, duststate2, duststate3):
    # 좋음
    if duststate3 <= 30 and (duststate1 and duststate2) <= 15 :
        lcd.lcd_string("     GOOD      ", lcd.LCD_LINE_1)
        led.color = Color("blue")
    # 보통
    elif  duststate3 <= 80 or (duststate1 or duststate2) <= 35:
        lcd.lcd_string("     NORMAL    ", lcd.LCD_LINE_1)
        led.color = Color("green")
    # 나쁨
    elif duststate3 <= 150 or (duststate1 or duststate2) <= 75:
        lcd.lcd_string("      BAD      ", lcd.LCD_LINE_1)
        led.color = Color("yellow")
    # 매우나쁨
    elif duststate3 > 150 or (duststate1 or duststate2) <= 75:
        lcd.lcd_string("    VERY BAD   ", lcd.LCD_LINE_1)
        led.color = Color("red")
    
    # pm1.0 표시
    lcd.lcd_string("pm1.0: %dug/m3 " %duststate1, lcd.LCD_LINE_2)
    powersw.wait_for_press(timeout=1)
    if powersw.is_pressed:
        return
    # pm2.5 표시
    lcd.lcd_string("pm2.5: %dug/m3 " %duststate2, lcd.LCD_LINE_2)
    powersw.wait_for_press(timeout=1)
    if powersw.is_pressed:
        return
    # pm10 표시
    lcd.lcd_string("pm10: %dug/m3  " %duststate3, lcd.LCD_LINE_2)
    powersw.wait_for_press(timeout=1)
    if powersw.is_pressed:
        return
    

    
    



# 메인루프
def mainloop():
    global power_state
    global led

    while True:
        # 먼지센서 동작
        ser = serial.Serial(SERIAL_PORT, Speed, timeout = 1)
        buffer = ser.read(1024)

        if(dustlib.protocol_chk(buffer)):
            data = dustlib.unpack_data(buffer)

            global pm1
            global pm25
            global pm10
            pm1 = data[dustlib.DUST_PM1_0_ATM]
            pm25 = data[dustlib.DUST_PM2_5_ATM]
            pm10 = data[dustlib.DUST_PM10_0_ATM]
            
            
            print ("PMS 7003 dust data")
            # print ("PM 1.0 : %s" % (data[dustlib.DUST_PM1_0_ATM]))
            # print ("PM 2.5 : %s" % (data[dustlib.DUST_PM2_5_ATM]))
            # print ("PM 10.0 : %s" % (data[dustlib.DUST_PM10_0_ATM]))
            print ("PM 1.0 : %s" % (pm1))
            print ("PM 2.5 : %s" % (pm25))
            print ("PM 10.0 : %s" % (pm10))
        else:
            print ("data read Err")
        
        # 전원 상태에 따른 동작

        if power_state == 0:
            print("전원꺼짐")
            fan.off()
            lcd.LCD_BACKLIGHT = 0x00
            lcd.lcd_string("   Power Off   ", lcd.LCD_LINE_1)
            lcd.lcd_string("", lcd.LCD_LINE_2)
        if power_state == 1:
            print("전원켜짐")
            lcd.LCD_BACKLIGHT = 0x08
            lcd.lcd_string("   Power On    ", lcd.LCD_LINE_1)
            fan.on()
            time.sleep(1)
            display_dust(int(pm1), int(pm25), int(pm10))
        if power_state == 2:
            print("자동모드")
            lcd.LCD_BACKLIGHT = 0x08
            lcd.lcd_string("   Auto Mode   ", lcd.LCD_LINE_1)
            time.sleep(1)
            display_dust(int(pm1), int(pm25), int(pm10))
            if pm25 >=30 :
                fan.on()
            else:
                fan.off()
        time.sleep(0.3)



if __name__ == "__main__":
    # 쓰레딩
    Thread(target=power).start()
    Thread(target=mainloop).start()
    # Thread(target=update_Dust).start()
    
