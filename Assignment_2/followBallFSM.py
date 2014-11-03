
# Import the FSM functions
from fsm.functions import (createState, createFSM, addTransition,
    addStates, setInitialState, readWM, writeWM, setPrintTransition)

# Import primitive robot behaviors
from api.pubapi import (
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
    if averageLook(wm)[0] > 0.2:
        print ("positivt", averageLook(wm)[0])
        return True
    else:
        return False

def negativeYaw(wm):
    if averageLook(wm)[0] < -0.2:
        print ("negativ", averageLook(wm)[0])
        return True
    else:
        return False

def zeroYaw(wm):
    if averageLook(wm)[0] <= 0.2 and averageLook(wm)[0] >= -0.2:
        print ("noll", averageLook(wm)[0])
        return True
    else:
        return False

def switchCamera(wm):
    if largestBall(wm)["x"] <= 300:
        return True 
    else:
        return False

def entryTime(wm):
    return readWM(wm, "time", "entry")

def currentTime(wm):
    return readWM(wm, "time", "current")

def delay(wm):
    return (currentTime(wm) - entryTime(wm) >= 0.5)


        


#create states    

rotateLeftState = createState("rotateLeftState", lambda : setWalkVelocity(0,0, 0.25))
rotateRightState = createState("rotateRightState", lambda : setWalkVelocity(0,0, -0.25))
walkToBallState = createState("walkToBallState", lambda : setWalkVelocity(1, 0, 0))
watchBallState = createState("watchBallState", lambda wm : lookAtBall(wm))
stopWalkingState = createState("stopWalkingState", stopWalking)
stopWalkingState2 = createState("stopWalkingState2", stopWalking) 
setBottomCamState = createState("setBottomCamState", lambda : setCamera("bottom"))
setBottomLedState = createState("setBottomLedState", lambda : setLED("eyes", 1,0,0))

# FSM for searching for the ball

followBallFSM = createFSM("followBallFSM")
addStates(followBallFSM, rotateLeftState, rotateRightState, walkToBallState,
          watchBallState, stopWalkingState, stopWalkingState2, setBottomLedState,
          setBottomCamState)


setInitialState(followBallFSM, watchBallState)

addTransition(watchBallState, positiveYaw, rotateLeftState)
addTransition(watchBallState, negativeYaw, rotateRightState)
addTransition(watchBallState, zeroYaw, walkToBallState)

addTransition(rotateRightState, zeroYaw, walkToBallState)
addTransition(rotateRightState, lambda wm: True, watchBallState)

addTransition(rotateLeftState, zeroYaw, walkToBallState)
addTransition(rotateLeftState, lambda wm: True, watchBallState)

#addTransition(stopWalkingState, lambda wm: True, walkToBallState)

addTransition(walkToBallState, switchCamera, setBottomCamState)
addTransition(setBottomCamState, delay, setBottomLedState)
addTransition(setBottomLedState, lambda wm: True, walkToBallState)

addTransition(walkToBallState, lambda wm : True, watchBallState)
