# Import the FSM functions
from fsm.functions import (createState, createFSM, addTransition,
    addStates, setInitialState, readWM, writeWM, setPrintTransition)	

# Import primitive robot behaviors
from api.pubapi import (sit, stand, rest, say, shutdown,
    startWalking, turnHead, setCamera, resetSubFSM,
    say, setLED, setWalkVelocity, stopWalking)

# Import functions we've written
from functions import (detectTouch, seeGoal, seeGoalLeft, seeGoalRight,
    seeGoalSingle, lookForGoal, seeBall)

# Create states

circleLeftState = createState("circleLeftState", lambda: setWalkVelocity(0, 1, -0.45))
circleRightState = createState("circleRightState", lambda: setWalkVelocity(0, 1, 0.45))
lookUpState = createState("lookUpState", lambda wm: lookUp(wm))
lookDownState = createState("lookDownState", lambda: turnHead(0, 0))
stopWalkingState = createState("stopWalkingState", stopWalking)
stopRotateState = createState("stopRotateState", stopWalking)
setTopCameraState = createState("setTopCameraState", lambda : setCamera("top"))
setBottomCameraState = createState("setBottomCameraState", lambda : setCamera("bottom"))
setTopCameraState2 = createState("setTopCameraState2", lambda : setCamera("top"))
setBottomCameraState2 = createState("setBottomCameraState2", lambda : setCamera("bottom"))
bottomLedState = createState("bottomLedState", lambda : setLED("eyes", 1, 0, 0)) # Red
topLedState = createState("topLedState", lambda : setLED("eyes", 0, 1, 0)) # Green
bottomLedState2 = createState("bottomLedState2", lambda : setLED("eyes", 1, 0, 0)) # Red
topLedState2 = createState("topLedState2", lambda : setLED("eyes", 0, 1, 0)) # Green
topLedState3 = createState("topLedState3", lambda : setLED("eyes", 0, 1, 0)) # Green

# Transitions for the findGoalFSM

addTransition(setTopCameraState, lambda wm: True, topLedState)
addTransition(topLedState, lambda wm: True, circleLeftState)

addTransition(circleLeftState, seeGoal, stopWalkingState)
addTransition(circleLeftState, seeGoalLeft, circleRightState)
addTransition(circleLeftState, seeGoalSingle, stopRotateState)
addTransition(circleLeftState, lambda wm: True, setBottomCameraState)
addTransition(setBottomCameraState, lambda wm: True, bottomLedState)
addTransition(bottomLedState, seeBall, setTopCameraState)
addTransition(setTopCameraState, lambda wm: True, topLedState2)
addTransition(topLedState2, lambda wm: True, circleLeftState)

addTransition(circleRightState, seeGoal, stopWalkingState)
addTransition(circleRightState, seeGoalRight, circleLeftState)
addTransition(circleRightState, seeGoalSingle, stopRotateState)
addTransition(circleRightState, lambda wm: True, setBottomCameraState2)
addTransition(setBottomCameraState2, lambda wm: True, bottomLedState2)
addTransition(bottomLedState2, seeBall, setTopCameraState2)
addTransition(setTopCameraState2, lambda wm: True, topLedState3)
addTransition(topLedState3, lambda wm: True, circleRightState)

addTransition(stopRotateState, lambda wm: True, lookUpState)

addTransition(lookUpState, seeGoal, stopWalkingState)
addTransition(lookUpState, seeGoalRight, circleLeftState)
addTransition(lookUpState, seeGoalLeft, circleRightState)

addTransition(stopWalkingState, lambda wm: True, lookDownState)

findGoalFSM = createFSM("findGoalFSM")
addStates(findGoalFSM, stopWalkingState, lookUpState, lookDownState,
          circleLeftState, circleRightState, stopRotateState, topLedState,
          topLedState2, topLedState3, bottomLedState, bottomLedState2, 
          setBottomCameraState, setBottomCameraState2, setTopCameraState, 
          setTopCameraState2)
          
setInitialState(findGoalFSM, setTopCameraState)

# Prints all the completed transitions

setPrintTransition(findGoalFSM, True)
