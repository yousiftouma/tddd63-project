
# Import the FSM functions
from fsm.functions import (createState, createFSM, addTransition,
    addStates, setInitialState, readWM, writeWM, setPrintTransition)	

# Import primitive robot behaviors
from api.pubapi import (sit, stand, rest, say, shutdown,
    startWalking, turnHead, setCamera,
    say, setLED, setWalkVelocity, stopWalking)

# Import functions we've written
from functions import (seeBall, noSeeBall, shakeHeadTime, largestBall,
    averageLook, lookAtBall, rotateTime, entryTime, currentTime, 
    cameraDelay, headTurning, lookAtBall2)


#Create States

shakeHeadState = createState("shakeHeadState", lambda wm: headTurning(wm))
shakeHeadState2 = createState("shakeHeadState2", lambda wm: headTurning(wm))
setTopCameraState = createState("setTopCameraState", lambda : setCamera("top"))
setBottomCameraState = createState("setBottomCameraState", lambda : setCamera("bottom"))
setTopCameraState2 = createState("setTopCameraState2", lambda : setCamera("top"))
lookAtBallState = createState("lookAtBallState", lambda wm : lookAtBall2(wm))
rotateState = createState("rotateState", lambda : setWalkVelocity(0, 0, 0.5))
bottomLedState = createState("bottomLedState", lambda : setLED("eyes", 1, 0, 0)) # Red
topLedState = createState("topLedState", lambda : setLED("eyes", 0, 1, 0)) # Green
topLedState2 = createState("topLedState2", lambda : setLED("eyes", 0, 1, 0)) # Green
stopWalkState = createState("stopWalkState", stopWalking)


# FSM for searching for the ball

lookBallFSM = createFSM("lookBallFSM")
addStates(lookBallFSM, shakeHeadState, stopWalkState,
          setTopCameraState, setTopCameraState2, 
          setBottomCameraState, bottomLedState,
          topLedState, lookAtBallState, rotateState,
          shakeHeadState2,topLedState2)

setInitialState(lookBallFSM, shakeHeadState)

# Transitions

addTransition(shakeHeadState, seeBall, lookAtBallState)
addTransition(shakeHeadState, shakeHeadTime, setBottomCameraState)
addTransition(setBottomCameraState, cameraDelay, bottomLedState)


addTransition(bottomLedState, lambda wm: True, shakeHeadState2)
addTransition(shakeHeadState2, seeBall, lookAtBallState)
addTransition(shakeHeadState2, shakeHeadTime, setTopCameraState)
addTransition(setTopCameraState, cameraDelay, topLedState)

addTransition(topLedState, seeBall, lookAtBallState)
addTransition(topLedState, noSeeBall, rotateState)

# repeat after first 90 degrees

addTransition(rotateState, rotateTime, stopWalkState)
addTransition(stopWalkState, lambda wm: True, shakeHeadState)

# if ball is lost from sight

addTransition(lookAtBallState, noSeeBall, setTopCameraState2)
addTransition(setTopCameraState2, cameraDelay, topLedState2)

addTransition(topLedState2, seeBall, lookAtBallState)
addTransition(topLedState2, noSeeBall, shakeHeadState)

# Prints out completed transitions

#setPrintTransition(lookBallFSM, True)

