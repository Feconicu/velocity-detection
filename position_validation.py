from settings import point_validation_precision as precision
from settings import point_validation_depth as depth

def validate_position(x, y, list_to_check):
    counter = 0
    for list_of_positions in list_to_check:
        localflag = False
        for (a,b) in list_of_positions:
            if a-precision < x and a+precision > x and b-precision < y and b+precision > y:
                localflag = True
                break
        if localflag:
            counter+=1
    if counter == depth:
        return True
    return False
