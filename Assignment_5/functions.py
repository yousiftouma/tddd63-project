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
        #print ("positivt", averageLook(wm)[0])
        return True
    else:
        return False

def negativeYaw(wm):
    if largestBall(wm) == None or largestBall(wm) == False:
        return False
    if largestBall(wm)["yaw"] < -0.1:
        #print ("negativ", averageLook(wm)[0])
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
       # print ("noll", averageLook(wm)[0])
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


def shakeHeadTime(wm):
     t = currentTime(wm) - entryTime(wm)
     if t >= 4*1.5:
         return True
     else:
         return False



def headTurning(wm):
    t = currentTime(wm) - entryTime(wm) 
    if t <= 1.2:
        return turnHead(0 + t, 0.3149)
    elif t >= 1.2 and t <= 1.2*3:
        return turnHead(1.2 - (t-1.2), 0.3149)
    elif t >= 1.2*3 and t <= 1.2*4:
        return turnHead(-1.2 + (t-1.2*3), 0.3149)


def largestGoal(wm):
    camera_data_goals = readWM(wm,"goals")
    if not camera_data_goals:
        return None
    else:
        # Get the latest observation
        cur_frame = camera_data_goals[0]

        # The object with the largest area is most likely the true goal
        largest_goal = None
        for b1 in cur_frame:
            if (not largest_goal) or (largest_goal["pa"] < b1["pa"]):
                largest_goal = b1
        if  largest_goal["pa"] > 2500:
            return largest_goal
        else:
            return None



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
        largest_ball1 = None
        for b1 in cur_frame:
            if (not largest_ball1) or (largest_ball1["pa"] < b1["pa"]):
                largest_ball1 = b1
        if (currentTime(wm) - largest_ball1["t"]) <= 0.5:
            if  largest_ball1["pa"] > 50:
                return largest_ball1
        else:
            return False

def closeToFeet(wm):
    if not largestBall(wm):
        return False
    print (largestBall(wm)["x"], abs(largestBall(wm)["y"]))
    return (largestBall(wm)["x"] <= 110) and (abs(largestBall(wm)["y"]) <= 80)

# Ovan ska bytas ut till att kolla pitch/yaw pa bollen och se om huvudet ar snett

def rotateTime(wm):
    if currentTime(wm) - entryTime(wm) >= 2:
        return True
    else:
        return False


def walkDelay(wm):
    return currentTime(wm) - entryTime(wm) >= 1

def closeToObstacle(wm):
    if not largestBall(wm):
       # print("no ball")
        return False
    dist = largestBall(wm)["x"]
    pos = largestBall(wm)["px"]
    print ('mid', "dist=", dist, "px=", pos, "yaw=", abs(largestBall(wm)["yaw"]),
           "pa=", largestBall(wm)['pa'])
    return (dist <= 360) and abs(largestBall(wm)['yaw']) < 1.6

def obstacleToLeft(wm):
    if not largestBall(wm):
       # print("no ball")
        return False
    dist = largestBall(wm)["x"]
    pos = largestBall(wm)["px"]
    print ('left',"dist=", dist, "px=", pos, "yaw=", largestBall(wm)["yaw"])
    return (dist <= 390) and 0.3 < largestBall(wm)['yaw'] < 0.55

def obstacleToRight(wm):
    if not largestBall(wm):
       # print("no ball")
        return False
    dist = largestBall(wm)["x"]
    pos = largestBall(wm)["px"]
    print ('right', "dist=", dist, "px=", pos, "yaw=", largestBall(wm)["yaw"])
    return (dist <= 390) and -0.55 < largestBall(wm)['yaw'] < -0.3
