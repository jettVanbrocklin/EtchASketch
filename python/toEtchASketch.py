import cv2
import numpy as np
import serial
import time
from svgpathtools import svg2paths


import pathFinder
import iterativePathFinder

# Set your serial port and baud rate
SERIAL_PORT = 'COM9'       # Change this to your Arduino's port
BAUD_RATE = 9600

UP_ARROW_CODE = 2490368
DOWN_ARROW_CODE = 2621440
LEFT_ARROW_CODE = 2424832
RIGHT_ARROW_CODE = 2555904


#Testing key-codes for arrow keys
    # elif key == 2490368:
    #     print("Up arrow pressed")
    # elif key == 2621440:
    #     print("Down arrow pressed")
    # elif key == 2424832:
    #     print("Left arrow pressed")
    # elif key == 2555904:
    #     print("Right arrow pressed")

scale_proportion = 0.5
screen_height = 430
screen_width = 604

image = cv2.imread("images/tn_2.jpeg")
if image is None:
    print("Image failed to load. Check the file path.")
    exit()

lower_threshold = 128
upper_threshold = 255

h = image.shape[0]
w = image.shape[1]
print(f"height: {h}, width: {w}")
if h >= w: #Height is greater than width
    scale_proportion = (screen_height/h)
else:
    scale_proportion = (screen_width/w)

scaled_height = int(h * scale_proportion)
scaled_width = int(w * scale_proportion)

print(f"scaled_height: {scaled_height}, scaled_width: {scaled_width}")

resized = cv2.resize(image, (scaled_width, scaled_height))
# resized = cv2.resize(thresh, (250, 330))

gray = cv2.cvtColor(resized, cv2.COLOR_BGR2GRAY)


prev_lt = lower_threshold
prev_ut = upper_threshold
while cv2.waitKey(1) & 0xFF != ord('s'):
    if cv2.waitKeyEx(1) == UP_ARROW_CODE:
        lower_threshold = lower_threshold + 1
    elif cv2.waitKeyEx(1) == DOWN_ARROW_CODE:
        lower_threshold = lower_threshold - 1
    elif cv2.waitKeyEx(1) == LEFT_ARROW_CODE:
        upper_threshold = upper_threshold - 1
    elif cv2.waitKeyEx(1) == RIGHT_ARROW_CODE:
        upper_threshold = upper_threshold + 1
    _, thresh = cv2.threshold(gray, lower_threshold, upper_threshold, cv2.THRESH_BINARY_INV)
    
    cv2.imshow("Thresh", cv2.bitwise_not(thresh))
    if(lower_threshold != prev_lt):
        print(f"Lower_Threshold = {lower_threshold}")
    elif(upper_threshold != prev_ut):
        print(f"Upper Threshold = {upper_threshold}")
    prev_ut = upper_threshold
    prev_lt = lower_threshold







#Now I need to find the 5 largest pixel clusters
num_labels, labels, stats, centroids = cv2.connectedComponentsWithStats(thresh, connectivity=8)
full_string = np.array2string(labels, threshold=np.inf)
with open("label_array_2.txt", "w") as f:
    f.write(str(full_string))
# Each "label" represents a separate cluster
# stats: [x, y, width, height, area]
# centroids: [cx, cy] for each component

# Step 3: Filter out small clusters if needed and sort by area
min_area = 75  # adjust as needed
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

cv2.imshow("resized", resized)

pixels_in_cluster = []
y_values = []
x_values = []

paths = []

print("Number of Labels: " + str(num_labels))
print("Number of Clusters: " + str(len(clusters)))

for i in range(0, len(clusters)):
    pixels_in_cluster.append(cluster_pixel_locations[i]['pixels'])
    y_values.append(pixels_in_cluster[i][:, 0])
    x_values.append(pixels_in_cluster[i][:,1])
    paths.append(iterativePathFinder.findPath(x_values[i], y_values[i], x_values[i][0], y_values[i][0]))

print("Number of paths: " + str(len(paths)))

#Create a digital plotting system so I can test on my computer
canvas = 255 * np.ones((screen_height,screen_width,3), dtype="uint8") # 250 by 330 canvas, set all pixels

# ------------------------------ MAIN ----------------------------------
prev_response = ""
first_send = True
cv2.imshow("Canvas", canvas)
with serial.Serial(SERIAL_PORT, BAUD_RATE, timeout=1) as arduino:
    time.sleep(5)  # wait for connection
    prev_p = 0
    for p in range(len(paths)):
        if p != 0:
            cv2.line(canvas, (paths[p-1][len(paths[p-1])-1][0], paths[p-1][len(paths[p-1])-1][1]), (paths[p][0][0], paths[p][0][1]), (0,0,0), 1)
        if prev_p != p:
            first_send = True
        for i in range(len(paths[p])):
        #for i in range(50):

            #Check for out of bounds issues
            assert p < len(paths), f"p={p} out of range for paths (len={len(paths)})"
            assert i < len(paths[p]), f"i={i} out of range for paths[{p}] (len={len(paths[p])})"

            data = f"{paths[p][i][0]},{paths[p][i][1]}\n"


            print(f"Sending: {data.strip()}")
            cv2.circle(canvas, (paths[p][i][0], paths[p][i][1]), 0, (0,0,0), 1)
            arduino.write(data.encode())
            if first_send == True:
                time.sleep(2)
                first_send = False

            time.sleep(0.08)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break       
            cv2.imshow("Canvas", canvas)
        prev_p = p
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break    
        


# PLOTTING ON COMPUTER
# cv2.imshow("Canvas", canvas)
# time.sleep(5)
# prev_p = 0
# for p in range(len(paths)):
#     if p != 0:
#         cv2.line(canvas, (paths[p-1][len(paths[p-1])-1][0], paths[p-1][len(paths[p-1])-1][1]), (paths[p][0][0], paths[p][0][1]), (0,0,0), 1)
#     for i in range(len(paths[p])):
#         #for i in range(50):

#         #Check for out of bounds issues
#         assert p < len(paths), f"p={p} out of range for paths (len={len(paths)})"
#         assert i < len(paths[p]), f"i={i} out of range for paths[{p}] (len={len(paths[p])})"

#         data = f"{paths[p][i][0]},{paths[p][i][1]}\n"


#         print(f"Sending: {data.strip()}")
#         cv2.circle(canvas, (paths[p][i][0], paths[p][i][1]), 0, (0,0,0), 1)
#         if cv2.waitKey(1) & 0xFF == ord('q'):
#             break


#         if prev_p != p:
#             time.sleep(1)
#         prev_p = p
            
#         cv2.imshow("Canvas", canvas)

# For creating g-code file
# prev_p = 0
# g_code_string = ""
# for p in range(len(paths)):
#     for i in range(len(paths[p])):
#         #for i in range(50):

#         #Check for out of bounds issues
#         assert p < len(paths), f"p={p} out of range for paths (len={len(paths)})"
#         assert i < len(paths[p]), f"i={i} out of range for paths[{p}] (len={len(paths[p])})"

#         data = f"{paths[p][i][0]},{paths[p][i][1]}\n"
        
#         g_code_string = g_code_string + data
#         g_code_string = g_code_string + ", "


# g_code_string = g_code_string + "end"
# with open("new_g_code.txt", "w") as f:
#     f.write(str(g_code_string))
cv2.waitKey(0)
cv2.destroyAllWindows()