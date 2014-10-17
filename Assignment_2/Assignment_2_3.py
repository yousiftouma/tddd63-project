# Import the FSM functions
from fsm.functions import (
	createState , createFSM ,
	addTransition , addStates ,
	setInitialState, readWM, writeWM, setPrintTransition )		# setMainFSM should be there

# Import primitive robot behaviors
from api.pubapi import sit, stand , rest, say , shutdown ,\
    startWalking , turnHead , hMShake , hMHang, setCamera,\
    say, setLED

# Define the functions for world model

def detectTouch(wm):
    return readWM(wm, "tactile", "middle")

def seeBall(wm):
    camera_data_balls = readWM(wm, "balls")
    if not largestBall(wm)["pa"] == None:
        print (largestBall(wm)["pa"])
        if largestBall(wm)["pa"] >= 70:
            print( largestBall(wm)["pa"], "see ball" )
            return True
    else:
        return False

def noSeeBall(wm):
    camera_data_balls = readWM(wm, "balls")
    if not largestBall(wm)["pa"] == None:
        print (largestBall(wm)["pa"])
        if largestBall(wm)["pa"] <= 70:
            print( largestBall(wm)["pa"] , "no ball")
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
            if ( not largest_ball1 ) or (largest_ball1["pa"] < b1["pa"]):
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

def entryTime(wm):
    return readWM(wm, "time", "entry")

def currentTime(wm):
    return readWM(wm, "time", "current")

def time(wm):
    if currentTime(wm) - entryTime(wm) >= 20:
        return True
    else:
        return False
    

# create states

waitSittingState = createState("waitSittingState", lambda : None)
waitStandingState = createState("waitStandingState", lambda: None)
waitStanding2State = createState("waitStanding2State", lambda: None)
sitState = createState("sitState", sit)
restState = createState("restState", rest)
standState = createState("standState", stand)
shakeHeadState = createState("shakeHeadState", hMShake)
shakeHead2State = createState("shakeHead2State", hMShake)
hangHeadState = createState("hangHeadState", hMHang)
shutdownState = createState("shutdownState",
				lambda : shutdown("Final state reached"))
setTopCameraState = createState("setTopCameraState", lambda : setCamera("top"))
setBottomCameraState = createState("setBottomCameraState", lambda : setCamera("bottom"))
sayBallState = createState("sayBallState", lambda : say("ball!"))
sayNoBallState = createState("sayNoBallState", lambda : say("no fucking ball found!"))
lookAtBallState = createState("lookAtBallState", lambda wm : lookAtBall(wm) )


# Add transitions

addTransition(waitSittingState , detectTouch , standState)
addTransition(standState, lambda wm: True, hangHeadState )
addTransition(hangHeadState, lambda wm: True, waitStandingState)
addTransition(waitStandingState, seeBall  , sayBallState )
addTransition(waitStandingState, time , sayNoBallState)
addTransition(sayBallState, lambda wm: True, lookAtBallState )
addTransition(lookAtBallState, noSeeBall , sayNoBallState )
addTransition(sayNoBallState, lambda wm: True, sitState)
addTransition(sitState , lambda wm: True , restState)
addTransition(restState , lambda wm: True , shutdownState)

# Create the FSM and add the states created above
myFSM = createFSM("fsm")
addStates(myFSM , waitSittingState , standState , 
           sitState , restState , shutdownState ,
          shakeHeadState , shakeHead2State , 
          hangHeadState, waitStandingState, setTopCameraState, 
          setBottomCameraState, sayBallState,
          sayNoBallState, lookAtBallState )

setPrintTransition(myFSM, True)

# Set the initial state to waitSittingState
setInitialState(myFSM , waitSittingState)
