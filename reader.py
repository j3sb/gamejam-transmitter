import time
import threading
import queue

import serial
import numpy as np
import scipy
import matplotlib.pyplot as plt


DATA_QUEUE = queue.Queue(maxsize=10)
DATA_FREQ = 10_000


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
            DATA_QUEUE.put_nowait(data)
            print(f"receiving @ {1.0/dt/1000:6.3f} kHz")
        except queue.Full:
            print("dropping data")


IMAGE_DT = 0.005

SCALE_FACTOR = int(0.5 + DATA_FREQ * IMAGE_DT)
IMAGE_WIDTH = 64
IMAGE_HEIGHT = IMAGE_WIDTH

def main():
    fig, axes = plt.subplots(2, 2, figsize=(8, 8))
    raw_graph = axes[0][0].plot([0], [0])[0]
    freq_graph = axes[1][0].plot([0], [0])[0]
    axes[0][0].set_xlim([0, 1000])  # 1000 samples
    axes[0][0].set_ylim([-0.5, 0.5])
    axes[1][0].set_xlim([0, 1000])  # 1000 samples
    axes[1][0].set_ylim([0, 5000])  # 5 kHz
    implot = axes[0][1].imshow(
        np.zeros((IMAGE_WIDTH, IMAGE_HEIGHT)),
        cmap='gray', vmin=0, vmax=255,
    )

    dt = 1/DATA_FREQ
    buffer = np.zeros(IMAGE_WIDTH * IMAGE_HEIGHT * SCALE_FACTOR)
    line_length = buffer.shape[0] // IMAGE_HEIGHT  # Hopefully an integer
    buffer_i = 0

    extra_offset = 0

    def on_press(event):
        nonlocal extra_offset

        if event.key == "up":
            extra_offset += 8 * SCALE_FACTOR
        if event.key == "down":
            extra_offset -= 8 * SCALE_FACTOR
        if event.key == "left":
            extra_offset += 1 * SCALE_FACTOR
        if event.key == "right":
            extra_offset -= 1 * SCALE_FACTOR
        extra_offset %= line_length

    fig.canvas.mpl_connect('key_press_event', on_press)

    while True:
        data = DATA_QUEUE.get()

        x = np.arange(data.shape[0])
        y = data - np.mean(data)

        raw_graph.set_data(x, y)

        # Find the positions of the rising edge
        next_y = np.concat([y[1:], y[-1:]])
        edge = (next_y > 0) > (y > 0)  # beautiful code
        has_edge = np.where(edge)[0]

        # Interpolate and scale to find exact edge positions
        edge_pos = has_edge + y[has_edge] / (y[has_edge] - next_y[has_edge])

        # Compute frequencies
        deltas = (edge_pos[1:] - edge_pos[:-1]) * dt
        x2 = edge_pos[:-1]
        y2 = 1.0 / deltas

        if x2.shape[0] == 0:
            x2 = np.array([0.0])
            y2 = np.array([0.0])
        y3 = np.interp(x, x2, y2)

        freq_graph.set_data(x, y3)

        for n in y3:
            buffer[buffer_i] = n
            buffer_i = (buffer_i + 1) % buffer.shape[0]

        shift = buffer_i - buffer_i % line_length + line_length + extra_offset
        rotated = np.concat([buffer[shift:], buffer[:shift]])

        image = scipy.signal.resample(rotated, IMAGE_WIDTH * IMAGE_HEIGHT) \
            .reshape((IMAGE_HEIGHT, IMAGE_WIDTH))

        image = (image - 500) / 6

        implot.set_data(image)

        plt.draw()
        plt.pause(1e-3)


if __name__ == "__main__":
    threading.Thread(target=read_thread, daemon=True).start()

    try:
        main()
    except KeyboardInterrupt:
        pass
