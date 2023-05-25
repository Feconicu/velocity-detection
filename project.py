#Program, który na podstawie filmu video określa, czy zbliżamy, czy oddalamy się od obiektu (np.. drzwi)
#Program to detect if an object is approaching towards camera or is getting further
#Code was written for education purposes as a final project 
#for "python w przetwarzaniu obrazu" lectures (Warsaw University of Technology)

import cv2
from settings import absolute_path__to_input as input
from settings import absolute_path__to_output as output
from settings import path_to_data as data
from position_validation import validate_position as validate_xy
from settings import point_validation_depth as depth
from settings import disctance_validation_depth as dis_depth
from disctance_detection import check_distance_change as check_dis
from settings import min_size

capture_vid = cv2.VideoCapture(input)
result = cv2.VideoWriter(output,
                                cv2.VideoWriter_fourcc(*'mp4v'), 
                                int(capture_vid.get(cv2.CAP_PROP_FPS)),
                                (int(capture_vid.get(cv2.CAP_PROP_FRAME_WIDTH)), 
                                int(capture_vid.get(cv2.CAP_PROP_FRAME_HEIGHT))))

prev_x, prev_y = 0,0
prev_height, prev_width = 0,0
prev_found = []
to_valid = []
distance_list = []

while capture_vid.isOpened():
    retval, frame = capture_vid.read()
    if retval:
        frame_gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        object_data = cv2.CascadeClassifier(data)
        found = object_data.detectMultiScale(frame_gray, minSize = min_size)

        if len(found) != 0:
            for (x, y, width, height) in found:
                if validate_xy(x, y, to_valid):
                    if check_dis(distance_list) == 1:
                        color = (0,255,0)
                    elif check_dis(distance_list) == -1:
                        color = (255,0,0)
                    else:
                        color = (0,0,0)

                    cv2.rectangle(frame, (x, y),
                                (x + height, y + width),
                                color, 5)
                    prev_x, prev_y = x,y
                
            #update lists
            prev_found.clear()
            for (x,y,width,height) in found:
                prev_found.append((x,y))
                if(height*width < prev_height*prev_width):
                    distance_list.append(False)
                else: 
                    distance_list.append(True)
                prev_height = height
                prev_width = width

            to_valid.append(prev_found)

            #shorten lists if needed
            if(len(to_valid)>depth):
                to_valid.pop(0)
            if(len(distance_list)>dis_depth):
                distance_list.pop(0)

        result.write(frame)
    else:
        break #end infinite loop

capture_vid.release()
result.release()
cv2.destroyAllWindows()

