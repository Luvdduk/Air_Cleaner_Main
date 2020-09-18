from gpiozero import PWMOutputDevice, Button, DigitalOutputDevice, OutputDevice
import time



fansw= Button(24)

# 팬 조절
fan_pwm = PWMOutputDevice(12)
fan_pin1 = OutputDevice(5)
fan_pin2 = OutputDevice(6)
ON = 1
OFF = 0
# 팬속
FULL = 1.0
MID = 0.65
SLOW = 0.3


fan_pwm.value = 1.0
fan_state = "FULL"

fan_pin1.on()
fan_pin2.off()
time.sleep(3)

fan_pwm.value = 0.3

time.sleep(3)

fan_pin1.off()
fan_pin2.off()