import cv2
import numpy as np
import serial
import time
from svgpathtools import svg2paths

# Set your serial port and baud rate
SERIAL_PORT = 'COM9'       # Change this to your Arduino's port
BAUD_RATE = 9600

scale_proportion = 1
screen_height = 250
screen_width = 330

image = cv2.imread("images/Dawg.jpg")
if image is None:
    print("Image failed to load. Check the file path.")
    exit()

gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

_, thresh = cv2.threshold(gray, 127, 255, cv2.THRESH_BINARY)

#thresh = cv2.bitwise_not(thresh)


h = thresh.shape[0]
w = thresh.shape[1]
print(f"height: {h}, width: {w}")

if h > w: #Height is greater than width
    scale_proportion = (screen_height/h)
else:
    scale_proportion = (screen_width/w)

scaled_height = int(h * scale_proportion)
scaled_width = int(w * scale_proportion)

print(f"scaled_height: {scaled_height}, scaled_width: {scaled_width}")

resized = cv2.resize(thresh, (scaled_width, scaled_height))



#Now I need to find the 5 largest pixel clusters
num_labels, labels, stats, centroids = cv2.connectedComponentsWithStats(resized, connectivity=8)

# Each "label" represents a separate cluster
# stats: [x, y, width, height, area]
# centroids: [cx, cy] for each component

# Step 3: Filter out small clusters if needed and sort by area
min_area = 100  # adjust as needed
clusters = []
for i in range(1, num_labels):  # skip label 0 (background)
    area = stats[i, cv2.CC_STAT_AREA]
    if area >= min_area:
        clusters.append((i, area, tuple(centroids[i])))

# Sort by area (largest first)
clusters.sort(key=lambda x: x[1], reverse=True)

cluster_pixel_locations = []
for label_id, area, centroid in clusters:
    pixels = np.column_stack(np.where(labels == label_id))
    cluster_pixel_locations.append({
        'label': label_id,
        'area': area,
        'centroid': centroid,
        'pixels': pixels  # shape (N, 2), each row is (y, x)
    })

# Example: Print info of largest cluster
largest = cluster_pixel_locations[0]
print("Largest Cluster Area:", largest['area'])
print("Centroid:", largest['centroid'])
print("Sample Pixel Locations:", largest['pixels'][:5])

cv2.imshow("resized", resized)

# I need to send the pixel locations of the three largest pixel clusters
# Send over serial

#wait until start
while cv2.waitKey(1) & 0xFF == ord('s'):
    continue

pixels = largest['pixels']
y_coords = pixels[:, 0]  # all rows, first column (y values)
x_coords = pixels[:, 1]  # all rows, second column (x values)

with serial.Serial(SERIAL_PORT, BAUD_RATE, timeout=1) as arduino:
    time.sleep(2)  # wait for connection
    for i in range(len(largest['pixels'])):
    #for i in range(50):
        data = f"{x_coords[i]},{y_coords[i]}\n"
        print(f"Sending: {data.strip()}")
        arduino.write(data.encode())
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

        if arduino.in_waiting:
            response = arduino.readline().decode().strip()
            while response == prev_response:
               time.sleep(0.05)
               response = arduino.readline().decode().strip()
            print(f"Arduino says: {response}")

        time.sleep(0.1)


cv2.waitKey(0)
cv2.destroyAllWindows()