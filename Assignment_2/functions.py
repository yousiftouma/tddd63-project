from fsm.functions import (readWM, writeWM)

from api.pubapi import (sit, stand, rest, say, shutdown,
    startWalking, turnHead, setCamera,
    say, setLED, setWalkVelocity, stopWalking)

def averageLook(wm):
    camera_data_balls = readWM(wm, "balls")
    if not camera_data_balls:
        return None
    else:
        largest_ball2 = None
        second_frame = camera_data_balls[1]
        for b in second_frame:
            if (not largest_ball2) or (largest_ball2["pa"] < b["pa"]):
                largest_ball2 = b
        largest_ball3 = None
        third_frame = camera_data_balls[2]
        for c in third_frame:
            if (not largest_ball3) or (largest_ball3["pa"] < c["pa"]):
                largest_ball3 = c

        pitch_average = (largestBall(wm)["pitch"] + largest_ball2["pitch"] +
                        largest_ball3["pitch"]) / 3
        yaw_average = (largestBall(wm)["yaw"] + largest_ball2["yaw"] + 
                       largest_ball3["yaw"]) / 3
        return [yaw_average, pitch_average]

def lookAtBall(wm):
    return turnHead(averageLook(wm)[0], averageLook(wm)[1])

def largestBall(wm):
    camera_data_balls  = readWM(wm,"balls")
    if not camera_data_balls:
        return None
    else:
        # Get the latest observation
        cur_frame = camera_data_balls[0]

        # The object with the largest area is most likely the true ball
        largest_ball1 = None
        for b1 in cur_frame:
            if (not largest_ball1) or (largest_ball1["pa"] < b1["pa"]):
                largest_ball1 = b1
        return largest_ball1

def positiveYaw(wm):
    if averageLook(wm)[0] > 0.1:
        #print ("positivt", averageLook(wm)[0])
        return True
    else:
        return False

def negativeYaw(wm):
    if averageLook(wm)[0] < -0.1:
        print ("negativ", averageLook(wm)[0])
        return True
    else:
        return False

def zeroYaw(wm):
    if averageLook(wm)[0] <= 0.1 and averageLook(wm)[0] >= -0.1:
       # print ("noll", averageLook(wm)[0])
        return True
    else:
        return False

def switchCamera(wm):
    return (largestBall(wm)["x"] <= 700)

def closeToFeet(wm):
    print largestBall(wm)["x"]
    return (largestBall(wm)["x"] <= 160)
       

def entryTime(wm):
    return readWM(wm, "time", "entry")

def currentTime(wm):
    return readWM(wm, "time", "current")

def cameraDelay(wm):
    return (currentTime(wm) - entryTime(wm) >= 0.5)
   
def detectTouch(wm):
    return readWM(wm, "tactile", "middle")

def seeBall(wm):
    camera_data_balls = readWM(wm, "balls")
    if largestBall(wm) == None:
        return False
    elif largestBall(wm)["pa"] >= 200:
        print(largestBall(wm)['camera'] , "SeeBall")
        return True
    else:
        return False

def noSeeBall(wm):
    camera_data_balls = readWM(wm, "balls")
    if largestBall(wm) == None:
        return False
    elif largestBall(wm)["pa"] <= 200:
        print(largestBall(wm)['camera'] , "noSeeBall")
        return True
    else:
        return False

def shakeHeadTime(wm):
     t = currentTime(wm) - entryTime(wm)
     if t >= 4*1.5:
         return True
     else:
         return False

def rotateTime(wm):
    if currentTime(wm) - entryTime(wm) >= 5:
        return True
    else:
        return False

def headTurning(wm):
    t = currentTime(wm) - entryTime(wm) 
    if t <= 1.2:
        return turnHead(0 + t, 0.5149)
    elif t >= 1.2 and t <= 1.2*3:
        return turnHead(1.2 - (t-1.2), 0.5149)
    elif t >= 1.2*3 and t <= 1.2*4:
        return turnHead(-1.2 + (t-1.2*3), 0.5149)
