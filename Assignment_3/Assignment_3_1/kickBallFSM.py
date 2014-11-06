
# Import the FSM functions
from fsm.functions import (createState, createFSM, addTransition,
    addStates, setInitialState, readWM, writeWM, setPrintTransition)

# Import primitive robot behaviors
from api.pubapi import (
    startWalking, turnHead, setCamera, kick,
    say, setLED, setWalkVelocity, stopWalking)

# Import functions we've written
from functions import (averageLook, lookAtBall, largestBall, positiveYaw,
    negativeYaw, zeroYaw, switchCamera, entryTime, currentTime, cameraDelay,
    closeToFeet, leftFoot, rightFoot, detectRightKick, detectLeftKick,
    farNegativeYaw, farPositiveYaw, lookAtBall2)


#create states    

rotateLeftState = createState("rotateLeftState", lambda : setWalkVelocity(0,0, 0.15))
rotateRightState = createState("rotateRightState", lambda : setWalkVelocity(0,0, -0.15))
archLeftState = createState("archLeftState", lambda : setWalkVelocity(0.5, 0, 0.5))
archRightState = createState("archRightState", lambda : setWalkVelocity(0.5, 0, -0.5))
walkToBallState = createState("walkToBallState", lambda : setWalkVelocity(1, 0, 0))
watchBallState = createState("watchBallState", lambda wm : lookAtBall2(wm))
stopWalkingState = createState("stopWalkingState", stopWalking)
stopWalkingState2 = createState("stopWalkingState2", stopWalking) 
setBottomCamState = createState("setBottomCamState", lambda : setCamera("bottom"))
setBottomLedState = createState("setBottomLedState", lambda : setLED("eyes", 1,0,0))
kickRightState = createState("kickRightState", lambda : kick("right"))
kickLeftState = createState("kickLeftState", lambda : kick("left"))


# FSM for following the ball

kickBallFSM = createFSM("kickBallFSM")
addStates(kickBallFSM, rotateLeftState, rotateRightState, walkToBallState,
          watchBallState, stopWalkingState, stopWalkingState2, setBottomLedState,
          setBottomCamState, kickRightState, kickLeftState, archRightState, archLeftState)

setInitialState(kickBallFSM, watchBallState)

# Transitions

#addTransition(watchBallState, farPositiveYaw, archLeftState)
#addTransition(watchBallState, farNegativeYaw, archRightState)
addTransition(watchBallState, positiveYaw, rotateLeftState)
addTransition(watchBallState, negativeYaw, rotateRightState)
addTransition(watchBallState, zeroYaw, walkToBallState)

addTransition(rotateRightState, zeroYaw, walkToBallState)
addTransition(rotateRightState, lambda wm: True, watchBallState)
#addTransition(archRightState, zeroYaw, walkToBallState)
#addTransition(archRightState, lambda wm: True, watchBallState)

addTransition(rotateLeftState, zeroYaw, walkToBallState)
addTransition(rotateLeftState, lambda wm: True, watchBallState)
#addTransition(archLeftState, zeroYaw, walkToBallState)
#addTransition(archLeftState, lambda wm: True, watchBallState)


addTransition(walkToBallState, closeToFeet, stopWalkingState)
addTransition(walkToBallState, switchCamera, setBottomCamState)
addTransition(walkToBallState, lambda wm: True, watchBallState)

addTransition(setBottomCamState, cameraDelay, setBottomLedState)
addTransition(setBottomLedState, lambda wm: True, walkToBallState)

addTransition(stopWalkingState, leftFoot, kickLeftState)
addTransition(stopWalkingState, rightFoot, kickRightState)

addTransition(kickLeftState, lambda wm: True, watchBallState)
addTransition(kickRightState, lambda wm: True, watchBallState)




#addTransition(stopWalkingState, lambda wm: True, watchBallState2)



# Prints out completed transitions

setPrintTransition(kickBallFSM, True)
