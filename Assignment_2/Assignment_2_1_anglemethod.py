def rotate(wm):
    if current_position(wm) < 0:
        current_angle = current_position(wm) + 2*pi
    else:
        current_angle = current_position(wm)
    if readWM(wm, "start_angle") < 0:
        angle = readWM(wm, "start_angle") + 2 * pi
    else:
        angle = readWM(wm, "start_angle")
    if abs(angle - current_angle) >=  pi/2 - 0.1:
        return True
    else:
        return False

def uTurn(wm):
    if current_position(wm) < 0:
        current_angle = current_position(wm) + 2*pi
    else:
        current_angle = current_position(wm)
    if readWM(wm, "start_angle") < 0:
        angle = readWM(wm, "start_angle") + 2 * pi
    else:
        angle = readWM(wm, "start_angle")
    print(readWM(wm,"start_angle"), current_position(wm), abs(angle - current_angle), pi)
    if abs(angle - current_angle) >=  pi :
        return True
    else:
        return False

def start_position(wm):
    writeWM(wm, current_position(wm), "start_angle") 

def current_position(wm):
    return readWM(wm, "odometry", "wz")

# States for saving current angle

startAngleState = createState("startAngleState", lambda wm : start_position(wm))
startAngle2State = createState("startAngle2State", lambda wm : start_position(wm))
    
