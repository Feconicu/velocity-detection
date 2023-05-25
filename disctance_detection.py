from settings import distance_detection_tolerance

def check_distance_change(prev_results):
    closer_counter = 0
    further_counter = 0
    for i in prev_results:
        if(i == True):
            closer_counter+=1
        else:
            further_counter+=1
    if(further_counter*(1-distance_detection_tolerance) > closer_counter):
        return -1
    elif (further_counter < closer_counter*(1-distance_detection_tolerance)):
        return 1
    return 0
