import RPi.GPIO as GPIO
import spidev
from keyboard import is_pressed

GPIO.setmode(GPIO.BCM)
buzzer_pin = 5
led_pin = 6
GPIO.setup(buzzer_pin, GPIO.OUT)
GPIO.setup(led_pin, GPIO.OUT)


spi = spidev.SpiDev()
spi.open(0, 0)
spi.max_speed_hz = 1000000


def readadc(adcnum):
    r = spi.xfer2([1, 8 + adcnum << 4, 0])
    adcout = ((r[1] & 3) << 8) + r[2]
    return adcout


while not is_pressed("enter"):
    value = readadc(0)
    if value < 300:
        GPIO.output(buzzer_pin, GPIO.HIGH)
        GPIO.output(led_pin, GPIO.LOW)
    else:
        GPIO.output(buzzer_pin, GPIO.LOW)
        GPIO.output(led_pin, GPIO.HIGH)

GPIO.cleanup()
