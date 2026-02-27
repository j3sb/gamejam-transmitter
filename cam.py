from picamera2 import Picamera2
import time
# Initialize the camera
picam2 = Picamera2()
# Configure for still capture
config = picam2.create_still_configuration()
picam2.configure(config)
# Start the camera and capture
picam2.start()
time.sleep(2)  # Wait for settings to take effect
picam2.capture_file("test_image.jpg")
picam2.stop()
