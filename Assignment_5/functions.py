from fsm.functions import (readWM, writeWM)

from api.pubapi import (sit, stand, rest, say, shutdown,
    startWalking, turnHead, setCamera, communicate,
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

def lookAtBall2(wm):
    camera_data_balls  = readWM(wm,"balls")
    if not camera_data_balls:
        return None
    else:
        # Get the latest observation
        cur_frame = camera_data_balls[0]

        # The object with the largest area is most likely the true ball
        largest_ball = None
        for b1 in cur_frame:
            if (not largest_ball) or (largest_ball["pa"] < b1["pa"]):
                largest_ball = b1
                if  largest_ball["pa"] > 100:
                    return turnHead(largest_ball["yaw"], largest_ball["pitch"])



def positiveYaw(wm):
    if largestBall(wm) == None or largestBall(wm) == False:
        return False
    if largestBall(wm)["yaw"] > 0.1:
        return True
    else:
        return False

def negativeYaw(wm):
    if largestBall(wm) == None or largestBall(wm) == False:
        return False
    if largestBall(wm)["yaw"] < -0.1:
        return True
    else:
        return False

def farNegativeYaw(wm):
    if largestBall(wm) == None or largestBall(wm) == False:
        return False
    if largestBall(wm)["yaw"] < -0.1 and largestBall(wm)["x"] >= 500:
        return True
    else:
        return False

def farPositiveYaw(wm):
    if largestBall(wm) == None or largestBall(wm) == False:
        return False
    if largestBall(wm)["yaw"] > 0.1 and largestBall(wm)["x"] >= 500:
        return True
    else:
        return False

def zeroYaw(wm):
    if largestBall(wm) == None or largestBall(wm) == False:
        return False
    if largestBall(wm)["yaw"] <= 0.1 and largestBall(wm)["yaw"] >= -0.1:
        return True
    else:
        return False

def switchCamera(wm):
    if largestBall(wm) == None or largestBall(wm) == False:
        return False
    return (largestBall(wm)["x"] <= 700)

     
def entryTime(wm):
    return readWM(wm, "time", "entry")

def currentTime(wm):
    return readWM(wm, "time", "current")

def cameraDelay(wm):
    return (currentTime(wm) - entryTime(wm) >= 0.5)
   
def detectTouch(wm):
    return readWM(wm, "tactile", "middle")


def lookUp(wm):
    t = currentTime(wm) - entryTime(wm) 
    if t <= 0.6720*2:
        return turnHead(0, 0 - t/2)

def touchDelay(wm):
    return ((currentTime(wm) - entryTime(wm)) > 3) and readWM(wm, "tactile", "middle")

def largestBall(wm):
    camera_data_balls  = readWM(wm,"balls")
    if not camera_data_balls:
        return False
    else:
        # Get the latest observation
        cur_frame = camera_data_balls[0]

        # The object with the largest area is most likely the true ball
        largest_ball1 = []
        for b1 in cur_frame:
            if (currentTime(wm) - b1["t"]) <= 0.5:
                if  b1["pa"] > 100:
                    largest_ball1 += [b1]
        return largest_ball1
        

def closeToFeet(wm):
    if not largestBall(wm):
        return False
    print (largestBall(wm)["x"], abs(largestBall(wm)["y"]))
    return (largestBall(wm)["x"] <= 110) and (abs(largestBall(wm)["y"]) <= 80)

def rotateTime(wm):
    return (currentTime(wm) - entryTime(wm)) >= 2
        
def headDelay(wm):
    return (currentTime(wm) - entryTime(wm)) >= 0.5

def walkDelay(wm):
    return (currentTime(wm) - entryTime(wm)) >= 1

def closeToObstacle(wm):
    if not largestBall(wm):
        return False
    for ball in largestBall(wm):
        print("dist=", ball["x"], "yaw=", ball["yaw"], "size=", ball["pa"])
        if (ball["x"] <= 300) and abs(ball['yaw']) < 1.6:
            return True
    return False
        
def obstacleToLeft(wm):
    if not largestBall(wm):
        return False
    dist = largestBall(wm)["x"]
    pos = largestBall(wm)["px"]
    print ('left',"dist=", dist, "px=", pos, "yaw=", largestBall(wm)["yaw"])
    return (dist <= 390) and 0.3 < largestBall(wm)['yaw'] < 0.55

def obstacleToRight(wm):
    if not largestBall(wm):
        return False
    dist = largestBall(wm)["x"]
    pos = largestBall(wm)["px"]
    print ('right', "dist=", dist, "px=", pos, "yaw=", largestBall(wm)["yaw"])
    return (dist <= 390) and -0.55 < largestBall(wm)['yaw'] < -0.3

def closeToObstacle2(wm):
    if not largestBall(wm):
        return False
    dist = largestBall(wm)["x"]
    pos = largestBall(wm)["px"]
    size = largestBall(wm)["pa"]
    yaw = largestBall(wm)["yaw"]
    print ('mid', "dist=", dist, "px=", pos, "yaw=", yaw, "pa=", size)
    return size >= 1500 and abs(yaw) < 1.6
