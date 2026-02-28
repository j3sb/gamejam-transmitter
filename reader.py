import serial
import time
import numpy as np
from matplotlib.animation import FuncAnimation
import matplotlib.pyplot as plt

ser = serial.Serial('/dev/ttyACM0', 9600, timeout=1)

hist_size = 1000
data = np.zeros(hist_size)
X = np.arange(hist_size)

graph = plt.plot(X, data)[0]

mid = 256 / 2

was_high = False
while True:
    start = time.time()
    switches = 0
    for i in range(hist_size):
        # Read single byte
        byte = ser.read(1)

        data[i] = byte[0]
        if byte[0] > mid and not was_high:
            switches += 1
            was_high = True
        else:
            was_high = False

        # if byte:
        #     print(f"Got byte: {byte[0]:02X}")
        # else:
        #     print("nothing to read")
    graph.set_ydata(data)
    plt.ylim([0, 256])
    plt.draw()
    plt.pause(1e-3)
    end = time.time()
    sampling_speed = 1 / (end - start) / 1000 * hist_size
    print(
        f"freq: {switches / hist_size} sampling: {sampling_speed:.2f} khz")
