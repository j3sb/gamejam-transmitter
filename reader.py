import time
import threading
import queue

import serial
import numpy as np
import matplotlib.pyplot as plt


DATA_QUEUE = queue.Queue(maxsize=10)


def read_thread():
    print("reading")
    ser = serial.Serial('/dev/ttyACM0', 9600, timeout=1)

    buffer_size = 1000
    last_t = time.time()
    while True:
        data = b""
        while len(data) < buffer_size:
            data += ser.read(buffer_size - len(data))

        now = time.time()
        dt = (now - last_t) / len(data)
        last_t = now

        data = np.array(list(data)) / 255
        try:
            DATA_QUEUE.put_nowait((data, dt))
            print(f"receiving @ {1.0/dt/1000:6.3f} kHz")
        except queue.Full:
            print("dropping data")


image_dt = 1 / 1000
image_width = 50
image_height = image_width
image = np.zeros((image_height, image_width))
pointer = 0


def add_to_image(pixels):
    global pointer
    # print(pointer)
    for pixel in pixels.tolist():
        x = pointer % image_width
        y = int(pointer / image_height)
        image[y, x] = pixel
        pointer += 1
        pointer = pointer % (image_width * image_height)


def main():
    fig, axes = plt.subplots(1, 2, figsize=(8, 4))
    graph = axes[0].plot([0], [0])[0]
    axes[0].set_xlim([0, 1000 / 10_000])  # 1000 samples @ 10 kHz
    axes[0].set_ylim([0, 1400])
    implot = axes[1].imshow(image, cmap='gray', vmin=0, vmax=1000)

    while True:
        data, dt = DATA_QUEUE.get()

        y = data - np.mean(data)

        # Find the positions of the rising edge
        next_y = np.concat([y[1:], y[-1:]])
        edge = (next_y > 0) > (y > 0)  # beautiful code
        has_edge = np.where(edge)[0]

        # Interpolate and scale to find exact edge positions
        edge_pos = has_edge + y[has_edge] / (y[has_edge] - next_y[has_edge])
        edge_pos = edge_pos * dt

        deltas = edge_pos[1:] - edge_pos[:-1]

        x2 = edge_pos[:-1]
        y2 = 1.0 / deltas

        if x2.shape[0] == 0:
            x2 = np.array([0.0])
            y2 = np.array([0.0])

        x3 = np.arange(0, dt * data.shape[0], image_dt)
        y3 = np.interp(x3, x2, y2)

        add_to_image(y3)

        implot.set_data(image)

        # print(image)

        graph.set_data(x2, y2)

        plt.draw()
        plt.pause(1e-3)


if __name__ == "__main__":
    threading.Thread(target=read_thread, daemon=True).start()

    try:
        main()
    except KeyboardInterrupt:
        pass
