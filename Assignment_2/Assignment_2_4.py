# Import the FSM functions
from fsm.functions import (createState, createFSM, addTransition,
    addStates, setInitialState, readWM, writeWM, setPrintTransition)	

# Import primitive robot behaviors
from api.pubapi import (sit, stand, rest, say, shutdown,
    startWalking, turnHead, hMShake, hMHang, setCamera,
    say, setLED, setWalkVelocity, stopWalking)

# Functions to use world model

def detectTouch(wm):
    return readWM(wm, "tactile", "middle")


def seeBall(wm):
    camera_data_balls = readWM(wm, "balls")
    if largestBall(wm) == None:
        return False
    elif largestBall(wm)["pa"] >= 200:
       # print(largestBall(wm)["pa"], largestBall(wm)["camera"], "see ball")
        print(largestBall(wm))
        return True
    else:
        return False

def noSeeBall(wm):
    camera_data_balls = readWM(wm, "balls")
    if largestBall(wm) == None:
        return False
    elif largestBall(wm)["pa"] <= 200:
       # print(largestBall(wm)["pa"], largestBall(wm)["camera"], "no ball")
        print(largestBall(wm))
        return True
    else:
        return False

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

def rotateTime(wm):
    if currentTime(wm) - entryTime(wm) >= 5:
        return True
    else:
        return False

def entryTime(wm):
    return readWM(wm, "time", "entry")

def currentTime(wm):
    return readWM(wm, "time", "current")

def topCameraCheck(wm):
    if largestBall(wm) == None:
        return False
    elif largestBall(wm)["camera"] == "top":
        return True
    else:
        return False

def bottomCameraCheck(wm):
    if largestBall(wm) == None:
        return False
    elif largestBall(wm)["camera"] == "bottom":
        return True
    else:
        return False

def headTurning(wm):
    t = currentTime(wm) - entryTime(wm) 
    if t <= 2.0857:
        turnHead(0 + t, -0.6720)
    elif t >= 2.0857 and t <= 2.0857*3:
        turnHead(2.0857 - (t-2.0857))   
        

# Create states

waitSittingState = createState("waitSittingState", lambda : None)
sitState = createState("sitState", sit)
restState = createState("restState", rest)
standState = createState("standState", stand)
stopWalkState = createState("stopWalkState", stopWalking)
shakeHeadState = createState("shakeHeadState", lambda wm: headTurning(wm))
shakeHeadState2 = createState("shakeHeadState2", lambda wm: headTurning(wm))
hangHeadState = createState("hangHeadState", hMHang)
shutdownState = createState("shutdownState",
				lambda : shutdown("Final state reached"))
setTopCameraState = createState("setTopCameraState", lambda : setCamera("top"))
setBottomCameraState = createState("setBottomCameraState", lambda : setCamera("bottom"))
setTopCameraState2 = createState("setTopCameraState2", lambda : setCamera("top"))
sayBallState = createState("sayBallState", lambda : say("ball!"))
sayNoBallState = createState("sayNoBallState", lambda : say("no fucking ball found!"))
lookAtBallState = createState("lookAtBallState", lambda wm : lookAtBall(wm))
rotateState = createState("rotateState", lambda : setWalkVelocity(0, 0, 0.5))
bottomLedState = createState("bottomLedState", lambda : setLED("eyes", 1, 0, 0)) # Red
topLedState = createState("topLedState", lambda : setLED("eyes", 0, 1, 0)) # Green
topLedState2 = createState("topLedState2", lambda : setLED("eyes", 0, 1, 0)) # Green

# FSM for searching for the ball

lookBallFSM = createFSM("lookBallFSM")
addStates(lookBallFSM, shakeHeadState, stopWalkState,  
          hangHeadState, setTopCameraState, setTopCameraState2, 
          setBottomCameraState, sayBallState, bottomLedState,
          topLedState, sayNoBallState, lookAtBallState, rotateState,
          shakeHeadState2,topLedState2)

setInitialState(lookBallFSM, hangHeadState)

addTransition(hangHeadState, seeBall, lookAtBallState)
addTransition(hangHeadState, noSeeBall, shakeHeadState)

addTransition(shakeHeadState, seeBall, lookAtBallState)
#addTransition(shakeHeadState, noSeeBall, setBottomCameraState)
addTransition(shakeHeadState, noSeeBall, setBottomCameraState)
addTransition(setBottomCameraState, bottomCameraCheck, bottomLedState)

addTransition(bottomLedState, seeBall, lookAtBallState)
addTransition(bottomLedState, noSeeBall, shakeHeadState2)
addTransition(shakeHeadState2, seeBall, lookAtBallState)
addTransition(shakeHeadState2, noSeeBall, setTopCameraState)
addTransition(setTopCameraState, topCameraCheck, topLedState)

addTransition(topLedState, seeBall, lookAtBallState)
addTransition(topLedState, noSeeBall, rotateState)

# repeat after first 90 degrees

addTransition(rotateState, rotateTime, stopWalkState)
addTransition(stopWalkState, lambda wm: True, hangHeadState)

# if ball is lost from sight

##addTransition(lookAtBallState, noSeeBall, setTopCameraState2)
addTransition(lookAtBallState, noSeeBall, setTopCameraState2)
addTransition(setTopCameraState2, topCameraCheck, topLedState2)

addTransition(topLedState2, seeBall, lookAtBallState)
addTransition(topLedState2, noSeeBall, hangHeadState)



setPrintTransition(lookBallFSM, True)




# The main FSM

# Transitions for the mainFSM

addTransition(waitSittingState, detectTouch, standState)
addTransition(standState, lambda wm: True, lookBallFSM)
addTransition(lookBallFSM, detectTouch, sitState)
addTransition(sitState, lambda wm: True, restState)
addTransition(restState, lambda wm: True, shutdownState)

mainFSM = createFSM("mainFSM")
addStates(mainFSM, waitSittingState, standState, sitState,
          restState, shutdownState, lookBallFSM)
          
setInitialState(mainFSM, waitSittingState)

# Prints all the completed transitions

setPrintTransition(mainFSM, True)
