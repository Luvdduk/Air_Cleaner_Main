import serial
from PMS7003 import PMS7003

dustlib = PMS7003()

# Baud Rate
Speed = 9600

# UART / USB Serial
# USB0 = 
# UART = '/dev/ttyAMA0'

# USE PORT
SERIAL_PORT = '/dev/ttyUSB0'

#serial setting
ser = serial.Serial(SERIAL_PORT, Speed, timeout = 1)


buffer = ser.read(1024)

if(dustlib.protocol_chk(buffer)):
    data = dustlib.unpack_data(buffer)

    print ("PMS 7003 dust data")
    print ("PM 1.0 : %s" % (data[dustlib.DUST_PM1_0_ATM]))
    print ("PM 2.5 : %s" % (data[dustlib.DUST_PM2_5_ATM]))
    print ("PM 10.0 : %s" % (data[dustlib.DUST_PM10_0_ATM]))

else:
    print ("data read Err")

ser.close()