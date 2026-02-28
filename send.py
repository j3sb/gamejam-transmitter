import gpiozero
from time import sleep
from picamera2 import Picamera2

led = gpiozero.PWMLED(18, initial_value=0.5, frequency=1000)
button = gpiozero.Button(4)

# # Initialize the camera
# picam2 = Picamera2()
# # Configure for still capture
# config = picam2.create_still_configuration()
# picam2.configure(config)
# # Start the camera and capture
# picam2.start()
# sleep(2)  # Wait for settings to take effect
# # picam2.capture_file("test_image.jpg")
# picam2.stop()

while (True):
    led.frequency = 1000 if button.is_pressed else 500

    sleep(0.05)
    # led.frequency = 1000
    # print("2000")
    # sleep(0.2)
    # led.frequency = 500
    # print("1000")
    # sleep(0.2)
