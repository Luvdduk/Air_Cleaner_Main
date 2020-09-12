from gpiozero import Button
from signal import pause
from threading import Thread
import time
import serial
from PMS7003 import PMS7003


power_state=0

#먼지센서 오브젝트
dustlib = PMS7003()

# Baud Rate
Speed = 9600

# USE PORT
SERIAL_PORT = '/dev/ttyUSB0'

# led r:16 g:20 b:21
# 릴레이: 19


# 파워 모드변경
def power():
    global power_state
    # 전원 스위치 gpio26
    button = Button(26)
    button.when_pressed = powerctrl
    pause()
# 꺼짐: 0, 켜짐: 1, 자동: 2
def powerctrl():
    global power_state
    if power_state == 0:
        power_state = 1
        print("전원켬")
        return
    if power_state == 1:
        power_state = 2
        print("자동모드로 변경")
        return
    if power_state == 2:
        power_state = 0
        print("전원끔")
        return


def update_Dust():
    while True:
        #serial setting
        ser = serial.Serial(SERIAL_PORT, Speed, timeout = 1)
        buffer = ser.read(1024)

        if(dustlib.protocol_chk(buffer)):
            data = dustlib.unpack_data(buffer)

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
        time.sleep(1)

# 메인루프
def mainloop():
    global power_state
    
    while True:
        # 먼지센서
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
        

        if power_state == 0:
            print("전원꺼짐")
        if power_state == 1:
            print("전원켜짐")
        if power_state == 2:
            print("자동모드")
        time.sleep(1)







if __name__ == "__main__":
    # 쓰레딩
    Thread(target=power).start()
    Thread(target=mainloop).start()
    Thread(target=update_Dust).start()
    
