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
        if (currentTime(wm) - largest_ball1["t"]) <= 3:
            if  largest_ball1["pa"] > 100:
                return largest_ball1
        else:
            return False

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

def closeToFeet(wm):
    if not largestBall(wm):
        return False
    print (largestBall(wm)["x"], abs(largestBall(wm)["y"]))
    return (largestBall(wm)["x"] <= 110) and (abs(largestBall(wm)["y"]) <= 80)
       

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
    elif not largestBall(wm):
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
    elif not largestBall(wm):
        print("noSeeBall")
        return True
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
        return turnHead(0 + t, 0.3149)
    elif t >= 1.2 and t <= 1.2*3:
        return turnHead(1.2 - (t-1.2), 0.3149)
    elif t >= 1.2*3 and t <= 1.2*4:
        return turnHead(-1.2 + (t-1.2*3), 0.3149)

def leftFoot(wm):
    if largestBall(wm):
        return(largestBall(wm)["px"] < (largestBall(wm)["px_size"]/2))
    return False

def rightFoot(wm):
    if largestBall(wm):
        return(largestBall(wm)["px"] >= (largestBall(wm)["px_size"]/2))
    return False

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

def seeGoal(wm):
    if not largestGoal(wm):
        return False
    elif largestGoal(wm)["goal_type"] in ["left", "right", "single", "center"]:
        print (largestGoal(wm)["goal_type"], largestGoal(wm)["pa"], largestGoal(wm)["px"], "seeGoal")
        return True

def seeGoalLeft(wm):
    if largestGoal(wm) == None:
        return False
    elif largestGoal(wm)["goal_type"] == "left":
        print ("left", largestGoal(wm)["pa"])
        return True

def seeGoalRight(wm):
    if largestGoal(wm) == None:
        return False
    elif largestGoal(wm)["goal_type"] == "right":
        print ("right", largestGoal(wm)["pa"])
        return True

def seeGoalSingle(wm):
    if largestGoal(wm) == None:
        return False
    elif largestGoal(wm)["goal_type"] == "single" and ( \
            largestGoal(wm)["px"] > 150 or largestGoal(wm)["px"] < 330):
        print ("single", largestGoal(wm)["pa"])
        return True

def lookUp(wm):
    t = currentTime(wm) - entryTime(wm) 
    if t <= 0.6720*2:
        return turnHead(0, 0 - t/2)

def seeBar(wm):
    if largestGoal(wm) == None:
        return False
    elif largestGoal(wm)["goal_type"] in ["left", "right", "center"]:
        return True

def lookForGoal(wm):
    t = currentTime(wm) - entryTime(wm) 
    if t <= 1.2:
        return turnHead(0 + t, 0)
    elif t >= 1.2 and t <= 1.2*3:
        return turnHead(1.2 - (t-1.2), 0)
    
def oneStep(wm):
    return (currentTime(wm) - entryTime(wm) >= 0.5)

def oneKick(wm):
    return (currentTime(wm) - entryTime(wm) >= 7)

def betweenFeet(wm):
    if largestBall(wm):
        return (abs(largestBall(wm)["px"] - (largestBall(wm)["px_size"]/2)) <= 50)

def touchDelay(wm):
    return ((currentTime(wm) - entryTime(wm)) > 3) and readWM(wm, "tactile", "middle")

def waitForStand(wm):
    messages = readWM(wm, "comms")
    for key in  messages:
        if messages[key]["msg"] == "Stand":
            return True
    return False

def waitForSit(wm):
    messages = readWM(wm, "comms")
    for key in messages:
        if  messages[key]["msg"] == "Sit":
            return True
    return False

def waitForKick(wm):
    messages = readWM(wm, "comms")
    for key in messages:
        if  messages[key]["msg"] == "Kick":
            return True
    return False

def waitForFindBall(wm):
    messages = readWM(wm, "comms")
    for key in messages:
        if messages[key]["msg"] == "Find ball":
            return True
    return False

def seeNao(wm):
    camera_data_goals = readWM(wm,"goals")
    if not camera_data_goals:
        return False
    else:
        # Get the latest observation
        cur_frame = camera_data_goals[0]

        # The object with the largest area is most likely the true goal
        for b1 in cur_frame:
            if (currentTime(wm) - b1["t"]) <= 0.5:
                print ("naoSize", b1["pa"])
                if  b1["pa"] <= 2000 and b1["pa"] >= 200:
                    return True
        return False

