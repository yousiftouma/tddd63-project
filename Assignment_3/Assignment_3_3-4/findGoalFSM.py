# Import the FSM functions
from fsm.functions import (createState, createFSM, addTransition,
    addStates, setInitialState, readWM, writeWM, setPrintTransition)	

# Import primitive robot behaviors
from api.pubapi import (sit, stand, rest, say, shutdown,
    startWalking, turnHead, setCamera, resetSubFSM,
    say, setLED, setWalkVelocity, stopWalking)

# Import functions we've written
from functions import (detectTouch, seeGoal, seeGoalLeft, seeGoalRight,
    seeGoalSingle, lookForGoal, seeBall, oneStep, leftFoot, rightFoot,
    betweenFeet)

# Create states

circleLeftState = createState("circleLeftState", lambda: setWalkVelocity(0, 1, -0.45))
circleRightState = createState("circleRightState", lambda: setWalkVelocity(0, 1, 0.45))
lookUpState = createState("lookUpState", lambda wm: lookUp(wm))
stopWalkingState = createState("stopWalkingState", stopWalking)
stopRotateState = createState("stopRotateState", stopWalking)
setTopCameraState = createState("setTopCameraState", lambda : setCamera("top"))
topLedState = createState("topLedState", lambda : setLED("eyes", 0, 1, 0)) # Green
lookStraightState = createState("lookStraightState", lambda : turnHead(0,0))
standState = createState("standState", stopWalking)
leftStepState = createState("leftStepState", lambda : setWalkVelocity(0, 0.5 ,0))
rightStepState = createState("rightStepState", lambda : setWalkVelocity(0, -0.5 ,0))

# Transitions for the findGoalFSM

addTransition(standState, leftFoot, leftStepState)
addTransition(standState, rightFoot, rightStepState)
addTransition(standState, betweenFeet, lookStraightState)

addTransition(leftStepState, oneStep, lookStraightState)
addTransition(rightStepState, oneStep, lookStraightState)

addTransition(lookStraightState, lambda wm: True, setTopCameraState)
addTransition(setTopCameraState, lambda wm: True, topLedState)
addTransition(topLedState, lambda wm: True, circleLeftState)

addTransition(circleLeftState, seeGoal, stopWalkingState)
addTransition(circleLeftState, seeGoalLeft, circleRightState)
addTransition(circleLeftState, seeGoalSingle, stopRotateState)

addTransition(circleRightState, seeGoal, stopWalkingState)
addTransition(circleRightState, seeGoalRight, circleLeftState)
addTransition(circleRightState, seeGoalSingle, stopRotateState)

addTransition(stopRotateState, lambda wm: True, lookUpState)

addTransition(lookUpState, seeGoal, stopWalkingState)
addTransition(lookUpState, seeGoalRight, circleLeftState)
addTransition(lookUpState, seeGoalLeft, circleRightState)



findGoalFSM = createFSM("findGoalFSM")
addStates(findGoalFSM, stopWalkingState, lookUpState,
          circleLeftState, circleRightState, stopRotateState, topLedState,
          setTopCameraState, lookStraightState, leftStepState, rightStepState,
          standState)
         
          
setInitialState(findGoalFSM, standState)

# Prints all the completed transitions

setPrintTransition(findGoalFSM, True)
