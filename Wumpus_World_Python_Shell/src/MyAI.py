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
from collections import defaultdict


LEFT=0,-1
DOWN=-1,0
UP=1,0
RIGHT=0,1

class MyAI ( Agent ):

    def __init__ ( self ):
        self.maze=defaultdict(lambda: defaultdict(set))
        ##index and set contains the surrsouding that accuse index to be wumpus
        self.safe=set()
        self.visited=set()
        self.goHome,self.action=[],[]
        self.find_gold=False
        self.direction=1
        self.current=(0,0)
        self.direction=RIGHT
        self.row,self.col=7,7
        self.bfs_queue=[]
        self.wumpus_die=False

    def getAction(self, stench, breeze, glitter, bump, scream):



        self.safe.add(self.current)
        self.visited.add(self.current)
        if self.current == (0, 0) and stench and not breeze and not self.wumpus_die:
            self.wumpus_die=True
            return Agent.Action.SHOOT
        self.make_percept(stench,breeze,bump,scream)

        if glitter:
            self.find_gold=True
            self.go_home()
            return Agent.Action.GRAB
        if self.find_gold and not self.action:
            if self.goHome==[]:
                return Agent.Action.CLIMB
            home_move=self.goHome.pop(0)
            self.fill_in_action(home_move)

        if not self.action:

            safe_move=self.find_safe_index()
            if not self.bfs_queue and safe_move!=self.current:
                self.fill_in_action(safe_move)
            elif safe_move==self.current:
                self.find_gold=True
                self.go_home()
                if self.goHome:
                    safe_move=self.goHome.pop(0)
                self.fill_in_action(safe_move)
            else:


                while self.bfs_queue[0]==self.current:
                    self.bfs_queue.pop(0)
                bfs_move =self.bfs_queue.pop(0)

                self.fill_in_action(bfs_move)

        next_move,next_direction=self.action.pop(0)

        if next_move==Agent.Action.TURN_LEFT or next_move== Agent.Action.TURN_RIGHT:
            self.direction=next_direction
        elif next_move==Agent.Action.SHOOT:

            self.safe.add((self.direction[0] + self.current[0], self.direction[1] + self.current[1]))
        else:
            self.current=self.direction[0]+self.current[0],self.direction[1]+self.current[1]

        return next_move

    def find_safe_index(self):
        '''find the safe index around current position，go with current direction first
            if all four direction has been explored , do a bfs and fill in the action
        '''
        four_direction=[LEFT,RIGHT,UP,DOWN]
        second_choice=set()

        row_i,col_i=self.current
        four_direction.insert(0,four_direction.pop(four_direction.index(self.direction)))

        for row,col in four_direction:
            row1,col1=row+row_i,col+col_i

            if self.checkCol(col1) and self.checkRow(row1) and (row1,col1) in self.safe:
                if (row1,col1) not in self.visited:

                    return row1,col1
                # else:
                #     second_choice.add((row1,col1))


        explore= self.safe-self.visited
        for i in explore:
            temp=self.bfs(self.current,i)
            if temp:
                self.bfs_queue=temp
                return temp


        return self.current

    def make_percept(self,stench,breeze,bump,scream):
        '''percept the surrounding and update the knowledge base for maze
            add this index to visited and safe
            if not percept, update arounding to safe

        '''

        if scream:
            self.wumpus_die=True
        if bump:
            r,l=self.current
            d1,d2=self.direction
            if self.direction==UP:
                self.row=r
                self.current=r-1,l

            elif self.direction==RIGHT:
                self.col=l
                self.current=r,l-1


            self.safe.add(self.current)
            self.visited.add(self.current)
            self.action=[]
            self.bfs_queue=[]




        if not stench and not breeze:

            self.visited.add(self.current)
            self.surrouding_safe(self.current)

        if stench and not breeze:
            if not self.wumpus_die:
                self.surrouding_wumpus(self.current)
            else:
                self.visited.add(self.current)
                self.surrouding_safe(self.current)

        if breeze and not stench:
            self.surrouding_pits(self.current)
        if breeze and stench:
            if not self.wumpus_die:
                self.surrouding_p_w(self.current)
            else:
                self.surrouding_pits(self.current)

    def surrouding_p_w(self,index):
        '''update by surrounding by pits and wumpus and current have both stench and breeze'''
        surrounding = self.surrouding(index)

        for i in surrounding:
            if i in self.visited and len(self.maze[i]["wumpus"]) <= 0 and len(self.maze[i]["pits"])<=0:
                self.safe.add(i)
            else:
                self.maze[i]["pits"].add(index)
                self.maze[i]["wumpus"].add(index)
                if len(self.maze[i]["wumpus"])>=3:
                    for j in self.maze[i]["wumpus"]:
                        self.safe.add(j)


                    self.kill_wumpus(i)


    def kill_wumpus(self,index):

        self.action=[]

        self.fill_in_action(index)

        self.action=self.action[:-1]
        self.action.append((Agent.Action.SHOOT,self.direction))


    def surrouding_pits(self,index):
        '''update by surrounding by pits and current only have breeze'''
        surrounding = self.surrouding(index)
        for i in surrounding:
            if i in self.visited and len(self.maze[i]["wumpus"]) >= 1:
                self.safe.add(i)
            else:
                self.maze[i]["pits"].add(index)
                # if len(self.maze[i]["pits"])>=4:
                #     print("pits",i)


    def surrouding_wumpus(self,index):
        '''update surrounding by wumpus and current only have stench'''
        surrounding = self.surrouding(index)
        for i in surrounding:
            if i in self.visited and len(self.maze[i]["pits"])>=1:
                    self.safe.add(i)
            else:
                self.maze[i]["wumpus"].add(index)
                if len(self.maze[i]["wumpus"])>=3:

                    for j in self.maze[i]["wumpus"]:
                        self.safe.add(j)
                    self.kill_wumpus(i)



    def surrouding_safe(self,index):
        '''update around to be safe'''
        surrounding=self.surrouding(index)

        for i in surrounding:
            self.safe.add(i)

    def surrouding(self,index):
        '''helper function to return the four direction around this index'''
        res=[]
        row_i, col_i = index

        for r, c in [LEFT,RIGHT,UP,DOWN]:
            row,col=row_i+r,col_i+c

            if (self.checkCol(col) and self.checkRow(row)) and (row,col) not in self.safe:
                res.append((row,col))


        return res


    def fill_in_action(self,next_move):
        '''fill in the action queue with actions(turn, goes up etc)'''

        if next_move==self.current and self.current==(0,0):

            self.action.append((Agent.Action.CLIMB,self.direction))
            return
        r1,c1=next_move
        r2,c2=self.current
        now=(r1 - r2, c1 - c2)
        if now==self.direction:

            self.action.append((Agent.Action.FORWARD,now))
        elif now == (-self.direction[0],-self.direction[1]):

            self.action.append((Agent.Action.TURN_LEFT,now))
            self.action.append((Agent.Action.TURN_LEFT,now))
            self.action.append((Agent.Action.FORWARD,now))
        elif self.direction in {UP,DOWN}:
            d1,d2=self.direction
            n1,n2=now

            if (d1,d2) ==(n2,n1):
                self.action.append((Agent.Action.TURN_RIGHT,now))
                self.action.append((Agent.Action.FORWARD,now))
            else:
                self.action.append((Agent.Action.TURN_LEFT,now))
                self.action.append((Agent.Action.FORWARD,now))
        elif self.direction in {RIGHT,LEFT}:
            d1, d2 = self.direction
            n1, n2 = now

            if (d1,d2) ==(n2,n1):
                self.action.append((Agent.Action.TURN_LEFT,now))
                self.action.append((Agent.Action.FORWARD,now))
            else:
                self.action.append((Agent.Action.TURN_RIGHT,now))
                self.action.append((Agent.Action.FORWARD,now))


        return

    def go_home(self):
        '''prepare the safe way to go back home, store each action in self.goHome'''
        res=[]
        self.goHome=self.bfs(self.current,(0,0))[1:]


        return

    def bfs(self, start,goal):
        queue = [[start]]
        seen = set(start)
        while queue:

            path = queue.pop(0)

            x, y = path[-1]
            if (x,y) == goal:
                return path
            for x2, y2 in ((x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1)):
                if (x2,y2) not in seen and (x2,y2) in self.safe:
                    queue.append(path + [(x2, y2)])
                    seen.add((x2, y2))

    def checkRow(self, row):
        '''check valid row number'''
        return row >= 0 and row < self.row

    def checkCol(self, col):
        '''check valid column number'''
        return col >= 0 and col < self.col




