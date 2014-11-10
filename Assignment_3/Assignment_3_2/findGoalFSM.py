# Import the FSM functions
from fsm.functions import (createState, createFSM, addTransition,
    addStates, setInitialState, readWM, writeWM, setPrintTransition)	

# Import primitive robot behaviors
from api.pubapi import (sit, stand, rest, say, shutdown,
    startWalking, turnHead, setCamera, resetSubFSM,
    say, setLED, setWalkVelocity, stopWalking)

# Import functions we've written
from functions import (detectTouch, seeGoal, seeGoalLeft, seeGoalRight,
    seeGoalSingle)

# Create states

rotateLeftState = createState("rotateLeftState", lambda: setWalkVelocity(0, 0, 0.7))
rotateRightState = createState("rotateRightState", lambda: setWalkVelocity(0,0, -0.7))
lookUpState = createState("lookUpState", lambda wm: lookUp(wm))
lookDownState = createState("lookDownState", lambda: turnHead(0, 0))
stopWalkingState = createState("stopWalkingState", stopWalking)
stopRotateState = createState("stopRotateState", stopWalking)

# Transitions for the findGoalFSM

addTransition(rotateLeftState, seeGoal, stopWalkingState)
addTransition(rotateLeftState, seeGoalLeft, rotateRightState)
addTransition(rotateLeftState, seeGoalSingle, stopRotateState)

addTransition(rotateRightState, seeGoal, stopWalkingState)
addTransition(rotateRightState, seeGoalRight, rotateLeftState)
addTransition(rotateRightState, seeGoalSingle, stopRotateState)

addTransition(stopRotateState, lambda wm: True, lookUpState)

addTransition(lookUpState, seeGoal, stopWalkingState)
addTransition(lookUpState, seeGoalRight, rotateLeftState)
addTransition(lookUpState, seeGoalLeft, rotateRightState)

addTransition(stopWalkingState, lambda wm: True, lookDownState)

findGoalFSM = createFSM("findGoalFSM")
addStates(findGoalFSM, stopWalkingState, lookUpState, lookDownState,
          rotateLeftState, rotateRightState, stopRotateState)
          
setInitialState(findGoalFSM, rotateLeftState)

# Prints all the completed transitions

setPrintTransition(findGoalFSM, True)
