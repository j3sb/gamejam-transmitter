import gpiozero
from time import sleep

led = gpiozero.PWMLED(18, initial_value = 0.5, frequency = 1000)

while (True):
	led.frequency = 2000
	print("2000")
	sleep(1)
	led.frequency = 1000
	print("1000")
	sleep(1)

