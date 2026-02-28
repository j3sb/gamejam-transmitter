import gpiozero
from time import sleep
from picamera2 import Picamera2
import numpy as np

signal_led = gpiozero.PWMLED(18, initial_value=0.5, frequency=1000)
button = gpiozero.Button(4)
ptt_led = gpiozero.LED(3, initial_value=False)

# # Initialize the camera
picam2 = Picamera2()
# # Configure for still capture
config = picam2.create_preview_configuration(main={"size": (100, 100)})
# config = picam2.create_still_configuration()
picam2.configure(config)
# # Start the camera and capture
# picam2.start()
# sleep(2)  # Wait for settings to take effect
# # picam2.capture_file("test_image.jpg")
# picam2.stop()

while True:
    if button.is_pressed:
        picam2.start()
        sleep(1)
        img = picam2.capture_array("main")

        # convert to grayscale thx
        gray = np.dot(img[..., :3], [0.299, 0.587, 0.114])

        # turn on ptt
        ptt_led.on()
        for y, x in np.ndindex(img.shape[:2]):
            pixel = img[y, x]
            signal_led.frequency = pixel * 2 + 500  # scale this somehow
            sleep(0.05)

        # for _ in range(10):
        #     signal_led.frequency = 500
        #     sleep(0.5)
        #     signal_led.frequency = 1000
        #     sleep(0.5)

        # turn off ptt
        ptt_led.off()

    sleep(0.05)
    # led.frequency = 1000
    # print("2000")
    # sleep(0.2)
    # led.frequency = 500
    # print("1000")
    # sleep(0.2)
