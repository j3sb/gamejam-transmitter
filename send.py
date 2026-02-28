import gpiozero
from time import sleep
import time
from picamera2 import Picamera2
import numpy as np

signal_led = gpiozero.PWMLED(18, initial_value=0.5, frequency=1000)
button = gpiozero.Button(4)
ptt_led = gpiozero.LED(3, initial_value=False)

# # Initialize the camera
picam2 = Picamera2()
# # Configure for still capture
config = picam2.create_preview_configuration(main={"size": (128, 128)})
# config = picam2.create_still_configuration()
picam2.configure(config)

picam2.start()
sleep(1)
# # Start the camera and capture
# picam2.start()
# sleep(2)  # Wait for settings to take effect
# # picam2.capture_file("test_image.jpg")
# picam2.stop()

print("ok")

while True:
    if button.is_pressed:
        img = picam2.capture_array("main")

        # convert to grayscale thx
        gray = np.dot(img[..., :3], [0.299, 0.587, 0.114])

        print(gray.shape)

        # turn on ptt
        ptt_led.on()
        now = time.time()
        for y in range(img.shape[0]):
            for x in range(img.shape[1]):
                pixel = img[y, x, 0]
                signal_led.frequency = int(
                    int(pixel) * 6 + 500)  # scale this somehow
                now += 0.005
                sleep(now - time.time())
                # print(x,y)
                # print(pixel)
            print(y)

        # for _ in range(10):
        #     signal_led.frequency = 3000
        #     sleep(0.5)
        #     signal_led.frequency = 1000
        #     sleep(0.5)

        # turn off ptt
        ptt_led.off()

    signal_led.frequency = 1000

    sleep(0.05)
    # led.frequency = 1000
    # print("2000")
    # sleep(0.2)
    # led.frequency = 500
    # print("1000")
    # sleep(0.2)
