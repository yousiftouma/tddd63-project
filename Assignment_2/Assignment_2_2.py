# Import the FSM functions
from fsm.functions import (
	createState , createFSM ,
	addTransition , addStates ,
	setInitialState, readWM, writeWM, setPrintTransition )		# setMainFSM should be there

# Import primitive robot behaviors
from api.pubapi import sit, stand , rest, say , shutdown ,\
    startWalking , turnHead , hMShake , hMHang

# Define the functions for world model

def detectTouch(wm):
    return readWM(wm, "tactile", "middle")

# create states

waitSittingState = createState("waitSittingState", lambda : None)
sitState = createState("sitState", sit)
restState = createState("restState", rest)
standState = createState("standState", stand)
shakeHeadState = createState("shakeHeadState", hMShake)
shakeHead2State = createState("shakeHead2State", hMShake)
hangHeadState = createState("hangHeadState", hMHang)
shutdownState = createState("shutdownState",
				lambda : shutdown("Final state reached"))

# Add transitions

addTransition(waitSittingState , detectTouch , standState)
addTransition(standState, lambda wm: True, shakeHeadState )
addTransition(shakeHeadState, lambda wm: True, hangHeadState )
addTransition(hangHeadState, lambda wm: True, shakeHead2State )
addTransition(shakeHead2State, lambda wm: True, sitState)
addTransition(sitState , lambda wm: True , restState)
addTransition(restState , lambda wm: True , shutdownState)

# Create the FSM and add the states created above
myFSM = createFSM("fsm")
addStates(myFSM , waitSittingState , standState , 
           sitState , restState , shutdownState ,
          shakeHeadState , shakeHead2State , 
          hangHeadState )

setPrintTransition(myFSM, True)

# Set the initial state to waitSittingState
setInitialState(myFSM , waitSittingState)
