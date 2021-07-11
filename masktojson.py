import cv2
import labelme
import base64
import numpy as np
import matplotlib.pyplot as plt
from .palette import *
from .overlaytomask import gen_rgb_mask

gen_rgb_mask()

# GETTING PLATE EDGE CONTOURS
##############################
list_of_innerobj = []
path_to_original_image = 'input/test.png'

# Load Original Image
raw_image = cv2.imread(path_to_original_image)

# Blur the image & apply Bilateral filter to remove noise (output looks visually similar to original image)
blurred = cv2.medianBlur(raw_image, 25)
bilateral_filtered_image = cv2.bilateralFilter(blurred, 5, 175, 175)  #plt.imshow(bilateral_filtered_image)  #display 'Bilateral Filtered Image'

# Detect all the sharp edges in the image
edge_detected_image = cv2.Canny(bilateral_filtered_image, 75, 200)  #plt.imshow(edge_detected_image) #display 'Edge Detected Image' 

# Find circles - this outputs list of (x, y, r) values, where (x,y) is the center & r is the radius
circles = cv2.HoughCircles(edge_detected_image, cv2.HOUGH_GRADIENT, 10, 7000)

# If some circle is found
if circles is not None:
   # Convert the (x, y, r) values into integers
   circles = np.round(circles[0, :]).astype("int")

   # calculating areas of all circles
   pi = 3.14159
   areas = []
   # loop over all the circles detected
   for (x, y, r) in circles:
     areas.append(pi * r * r)
   # choosing the circle with maximum area
   pos = [i for i, area in enumerate(areas) if area==max(areas)][0]
   plate = circles[pos]  #plate = [x, y, r]

   #creating a black empty image of dimensions same as original image ie raw_image.shape (1080,1440,3) without 3 RGB channels
   emt_img = np.zeros((raw_image.shape[0], raw_image.shape[1]), np.uint8)
   cv2.circle(emt_img, (plate[0], plate[1]), plate[2], (255, 255, 255), 2) #drawing our plate (in white, thickness=2) over our black image

   #finding contours of the circle
   contours, hierarchy = cv2.findContours(emt_img, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
   c = max(contours, key=cv2.contourArea)  #emt_img = cv2.drawContours(emt_img, c, -1, (255, 0, 0), 5)  #to draw all contours 

   # finding list of contour points, with every 80th point (for total 2284 points detected)
   cnt_pts = []
   c80th = c[0::80]
   for item in c80th:
     pt = [j for n in item for j in n]
     cnt_pts.append(pt)
   cnt_pts = np.array(cnt_pts) # converting to numpy array

   plate_obj = {
    "label": "plate",
    "line_color": None,
    "fill_color": None,
    "points": cnt_pts.tolist(),
    "shape_type": "polygon"
    }
list_of_innerobj.append(plate_obj)

# GETTING MASKED FOOD ITEMS CONTOUR POINTS
################################################
# load the mask image
mask_image = cv2.imread("demo/rgb_mask.png")

# convert to RGB
mask_image = cv2.cvtColor(mask_image, cv2.COLOR_BGR2RGB)

for i, color in enumerate(palette.palette):
  if color!=[0, 0, 0]:
    lower = [i-10 if i!=0 else i for i in color] #lower = [0,220,30]    #lower = [max(0, i-10) for i in color] 
    upper = [i+10 if i!=0 else i for i in color] #upper = [0,240,50]
    #create numpy arrays
    lower = np.array(lower, dtype="uint8")
    upper = np.array(upper, dtype="uint8")
  
    # find the colors within the specified boundaries and apply the mask
    mask = cv2.inRange(mask_image, lower, upper)

    # Determine if the color exists on the mask_image
    if cv2.countNonZero(mask) > 60000:  #if pixel count for that color is greater than 60000
      # thresholding mask image
      ret,thresh = cv2.threshold(mask, 40, 255, 0)
    
      # Finding all contours of particular color
      contours, hierarchy = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)       
      # Getting the contour with maximum area
      c = max(contours, key=cv2.contourArea)
      # Getting contour points list according to json format requirement
      cnt_pts = []
      for item in c:
        pt = [j for n in item for j in n]
        cnt_pts.append(pt)
      cnt_pts = np.array(cnt_pts)

      # Defining JSON object for the item
      inner_object = {
      "label": palette.getlabel(i),
      "line_color": None,
      "fill_color": None,
      "points": cnt_pts.tolist(),     #"points": c.tolist(),
      "shape_type": "polygon"
      }
      list_of_innerobj.append(inner_object)

# WRITING INTO THE JSON FILE
##################################
data = labelme.LabelFile.load_image_file(path_to_original_image)
image_data = base64.b64encode(data).decode('utf-8')
outer_object = {
    "version": "3.5.0",
    "flags": {},
    "shapes": list_of_innerobj,
    "lineColor": [0, 255, 0, 128],
    "fillColor": [255, 0, 0, 128],
    "imagePath": path_to_original_image,
    "imageData": image_data
}

# python dump to json:
import json
annotation = outer_object
with open("input/test.json", "w") as write_file:
    json.dump(annotation, write_file, indent=4)