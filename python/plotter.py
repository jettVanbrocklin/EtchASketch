import serial
import time
import numpy as np
from svgpathtools import svg2paths

# Set your serial port and baud rate
SERIAL_PORT = 'COM9'       # Change this to your Arduino's port
BAUD_RATE = 9600

# Load SVG paths
paths, _ = svg2paths('happy-birthday-dad.svg')

prev_response = 'NONE';

# Function to sample points along the SVG path
def sample_path_points(path, num_points=200):
    points = []
    for segment in path:
        for i in range(num_points):
            t = i / num_points
            point = segment.point(t)
            points.append((point.real, point.imag))
    return points

# Aggregate all paths
all_points = []
for path in paths:
    all_points.extend(sample_path_points(path, num_points=100))

# Normalize and scale coordinates
xs, ys = zip(*all_points)
xs = np.array(xs)
ys = np.array(ys)

xs = (xs - np.min(xs)) / (np.max(xs) - np.min(xs)) * 100
ys = (ys - np.min(ys)) / (np.max(ys) - np.min(ys)) * 100

# Send over serial
with serial.Serial(SERIAL_PORT, BAUD_RATE, timeout=1) as arduino:
    time.sleep(2)  # wait for connection
    for x, y in zip(xs, ys):
        data = f"{x:.2f},{y:.2f}\n"
        print(f"Sending: {data.strip()}")
        arduino.write(data.encode())

        # if arduino.in_waiting:
        #     response = arduino.readline().decode().strip()
        #     while response == prev_response:
        #        time.sleep(0.05)
        #        response = arduino.readline().decode().strip()
        #     print(f"Arduino says: {response}")

        time.sleep(0.02)
        