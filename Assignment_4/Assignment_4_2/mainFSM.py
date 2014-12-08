# Import the FSM functions
from fsm.functions import (
	createState, createFSM,
	addTransition, addStates,
	setInitialState, readWM, setPrintTransition)	

# Import primitive robot behaviors
from api.pubapi import (sit, stand, rest, say, shutdown, communicate)

# Import functions we've written
from functions import (detectTouch, touchDelay)

## CREATE STATES ##


standState = createState("standState", stand)
restState = createState("restState", rest)
shutdownState = createState("shutdownState",
				lambda : shutdown("Final state reached"))

 
# Create states for waiting for touch

waitSittingState4 = createState("waitSittingState3", lambda: None)
waitSittingState3 = createState("waitSittingState3", lambda: None)
waitSittingState2 = createState("waitSittingState2", lambda: None)
waitSittingState = createState("waitSittingState", lambda: None)

# Create communcationsstates

robot = "goliath"

sendStandStatus = createState("sendStandStatus" , 
                               lambda: communicate(robot, "Stand"))

sendSitStatus = createState("sendSitStatus", 
                            lambda: communicate(robot, "Sit"))

sendKickStatus = createState("sendKickStatus", 
                            lambda: communicate(robot, "Kick"))


# States for talking

sayShutdownState = createState("sayShutdownState", lambda: say("Shutting Down"))

# Add transitions according to the state diagram
addTransition(waitSittingState, detectTouch, sendStandStatus)

addTransition(sendStandStatus, lambda wm: True, waitSittingState2)
addTransition(waitSittingState2, touchDelay, sendKickStatus)

addTransition(sendKickStatus, lambda wm: True, waitSittingState3)
addTransition(waitSittingState3, touchDelay, sendSitStatus)

addTransition(sendSitStatus, lambda wm: True, waitSittingState4)
addTransition(waitSittingState4, touchDelay, sayShutdownState)

addTransition(sayShutdownState, lambda wm: True, restState)
addTransition(restState, lambda wm: True, shutdownState)


# Create the FSM and add the states created above
mainFSM = createFSM("mainFSM")
addStates(mainFSM, waitSittingState, waitSittingState2, waitSittingState3,
          waitSittingState4, sendStandStatus, sendSitStatus, sendKickStatus,
          restState, shutdownState, sayShutdownState)

# Set the initial state to waitSittingState
setInitialState(mainFSM, waitSittingState)

setPrintTransition(mainFSM, True)
