
# Import the FSM functions
from fsm.functions import (createState, createFSM, addTransition,
    addStates, setInitialState, readWM, writeWM, setPrintTransition)

# Import primitive robot behaviors
from api.pubapi import (
    startWalking, turnHead, setCamera,
    say, setLED, setWalkVelocity, stopWalking)

# Import functions we've written
from functions import (averageLook, lookAtBall, largestBall, positiveYaw,
    negativeYaw, zeroYaw, switchCamera, entryTime, currentTime, cameraDelay,
    closeToFeet)


#create states    

rotateLeftState = createState("rotateLeftState", lambda : setWalkVelocity(0,0, 0.15))
rotateRightState = createState("rotateRightState", lambda : setWalkVelocity(0,0, -0.15))
walkToBallState = createState("walkToBallState", lambda : setWalkVelocity(1, 0, 0))
watchBallState = createState("watchBallState", lambda wm : lookAtBall(wm))
stopWalkingState = createState("stopWalkingState", stopWalking)
stopWalkingState2 = createState("stopWalkingState2", stopWalking) 
setBottomCamState = createState("setBottomCamState", lambda : setCamera("bottom"))
setBottomLedState = createState("setBottomLedState", lambda : setLED("eyes", 1,0,0))

# FSM for following the ball

followBallFSM = createFSM("followBallFSM")
addStates(followBallFSM, rotateLeftState, rotateRightState, walkToBallState,
          watchBallState, stopWalkingState, stopWalkingState2, setBottomLedState,
          setBottomCamState)

setInitialState(followBallFSM, watchBallState)

# Transitions

addTransition(watchBallState, positiveYaw, rotateLeftState)
addTransition(watchBallState, negativeYaw, rotateRightState)
addTransition(watchBallState, zeroYaw, walkToBallState)

addTransition(rotateRightState, zeroYaw, walkToBallState)
addTransition(rotateRightState, lambda wm: True, watchBallState)

addTransition(rotateLeftState, zeroYaw, walkToBallState)
addTransition(rotateLeftState, lambda wm: True, watchBallState)

addTransition(walkToBallState, closeToFeet, stopWalkingState)
addTransition(walkToBallState, switchCamera, setBottomCamState)
addTransition(setBottomCamState, cameraDelay, setBottomLedState)
addTransition(setBottomLedState, lambda wm: True, walkToBallState)

addTransition(stopWalkingState, lambda wm: True, watchBallState)



# Prints out completed transitions

#setPrintTransition(followBallFSM, True)
