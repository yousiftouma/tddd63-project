
# Import the FSM functions
from fsm.functions import (createState, createFSM, addTransition,
    addStates, setInitialState, readWM, writeWM, setPrintTransition)

# Import primitive robot behaviors
from api.pubapi import (
    startWalking, turnHead, setCamera, kick,
    say, setLED, setWalkVelocity, stopWalking)

# Import functions we've written
from functions import (leftFoot, rightFoot)
 
#create states    

kickRightState = createState("kickRightState", lambda : kick("right"))
kickLeftState = createState("kickLeftState", lambda : kick("left"))
stopWalkingState = createState("stopWalkingState", stopWalking)
stopWalkingState2 = createState("stopWalkingState2", stopWalking)


# FSM for kicking the ball

kickBallFSM = createFSM("kickBallFSM")
addStates(kickBallFSM, kickRightState, kickLeftState, stopWalkingState, stopWalkingState2)

setInitialState(kickBallFSM, stopWalkingState)

# Transitions

addTransition(stopWalkingState, leftFoot, kickLeftState)
addTransition(stopWalkingState, rightFoot, kickRightState)

addTransition(kickLeftState, lambda wm: True, stopWalkingState2)
addTransition(kickRightState, lambda wm: True, stopWalkingState2)

# Prints out completed transitions

setPrintTransition(kickBallFSM, True)
