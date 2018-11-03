# ======================================================================
# FILE:        MyAI.py
#
# AUTHOR:      Abdullah Younis
#
# DESCRIPTION: This file contains your agent class, which you will
#              implement. You are responsible for implementing the
#              'getAction' function and any helper methods you feel you
#              need.
#
# NOTES:       - If you are having trouble understanding how the shell
#                works, look at the other parts of the code, as well as
#                the documentation.
#
#              - You are only allowed to make changes to this portion of
#                the code. Any changes to other portions of the code will
#                be lost when the tournament runs your code.
# ======================================================================

from Agent import Agent

class MyAI ( Agent ):
    ROW_BOUND = 7
    COL_BOUND = 7
    WORLD = []
    def __init__ ( self ):
        # ======================================================================
        # YOUR CODE BEGINS
        # ======================================================================
        self._counter = 0

        # ======================================================================
        # YOUR CODE ENDS
        # ======================================================================

    def getAction( self, stench, breeze, glitter, bump, scream ):
        # ======================================================================
        # YOUR CODE BEGINS
        # ======================================================================
        self._counter += 1
        if self._counter == 1:
            if stench or breeze:
                return Agent.Action.CLIMB
            else:
                return Agent.Action.FORWARD
        elif self._counter == 2 or self._counter == 3:
            return Agent.Action.TURN_LEFT
        elif self._counter == 4:
            return Agent.Action.FORWARD
        else:
            return Agent.Action.CLIMB
        # ======================================================================
        # YOUR CODE ENDS
        # ======================================================================
    
    # ======================================================================
    # YOUR CODE BEGINS
    # ======================================================================

    
    # ======================================================================
    # YOUR CODE ENDS
    # ======================================================================