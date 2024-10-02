import numpy as np
import heapq
# class to maintain puzzle state and previous puzzle state(s), and move counts, also self compares to solution
class Puzzled:
    board=""
    # set up ininital board and members and also solution board
    def __init__(self,inputBoard,mve,count,predx=None):
        self.board=[]
        self.board=inputBoard
        self.solution=np.array([[1,2,3,4],[5,6,7,8],[9,10,11,12],[13,14,15,0]])
        self.width=len(self.board)
        self.height=len(self.board)
        self.heur=0
        self.moveCounter=count
        self.move=mve
        self.predecessor=predx # basically move that comes before, will be another Puzzled object
    # return current board state
    def getBoard(self):
        g=self.board
        return [g.copy()]
    # bool if state==final
    def goalReached(self):
        return (self.board==self.solution).all()
    # move open space somewhere
    def moveSpace(self,pos):
        row,col=0,0
        for x in self.board:
            col=0
            for y in x:
                if y==0:
                    break
                col+=1
            row+=1
        #tempPuzzle=Puzzled()
        if pos ==1: # right move
            if (col+1)<self.width:
                temp=self.board[row][col+pos]
                self.board[row][col+pos]=0
                self.board[row][col]=temp
        elif pos==-1: #left move
            if (col-1)>self.width:
                temp=self.board[row][col+pos]
                self.board[row][col+pos]=0
                self.board[row][col]=temp
        elif pos==0: #up move
            if (row-1)>-1:
                temp=self.board[row-1][col]
                self.board[row-1][col]=0
                self.board[row][col]=temp
        elif pos==2: #down move
            if (row+1)<self.height:
                temp=self.board[row+1][col]
                self.board[row+1][col]=0
                self.board[row][col]=temp
# attempts to generate 4 new Puzzled objects in each of the possible directions
# the open space can go
    def genMoves(self):
        row,col=0,0
        done=False
        # finding coordinates of open space
        for x in self.board:
            col=0
            for y in x:
                if y==0:
                    done=True
                    break
                col+=1
            if done:
                break
            row+=1
        # just codes for each move to preform
        moves=[1,0,-1,2]
        #print(col,row)
       # print(self.board)
        puzzles=[]
        # trying to move open space in each direction
        for pos in moves:
            if pos ==1: # right move
                if (col+1)<self.width:

                    tempBoard=self.getBoard()[0]
                    # swapping moves
                    tempBoard[row][col]=self.board[row][col+pos]
                    tempBoard[row][col+pos]=0
                    tempPuzzle=Puzzled(tempBoard,"right",self.moveCounter+1,self)
                    puzzles.append(tempPuzzle)

            elif pos==-1: #left move
                if (col-1)>-1:
                    #print(self.board)
                    #temp=tempPuzzle.board[row][col+pos]
                    tempBoard=self.getBoard()[0]
                    tempBoard[row][col]=self.board[row][col+pos]
                    tempBoard[row][col+pos]=0
                    tempPuzzle=Puzzled(tempBoard,"left",self.moveCounter+1,self)

                    puzzles.append(tempPuzzle)

            elif pos==0: #up move
                if (row-1)>-1:
                    #print(self.board)
                    tempBoard=self.getBoard()[0]

                    tempBoard[row][col]=self.board[row-1][col]
                    tempBoard[row-1][col]=0

                    tempPuzzle=Puzzled(tempBoard,"up",self.moveCounter+1,self)
                    puzzles.append(tempPuzzle)

            elif pos==2: #down move
                if (row+1)<self.height:
                    #print(self.board)

                    tempBoard=self.getBoard()[0]
                    tempBoard[row][col]=self.board[row+1][col]
                    tempBoard[row+1][col]=0
                    tempPuzzle=Puzzled(tempBoard,"down",self.moveCounter+1,self)
                    puzzles.append(tempPuzzle)
        return puzzles # returning all newly created puzzles 
    # calculate herustic value linear conflict manahattan distance and number of misplaced spaces
    def manhConflict(self):
        current=self.getBoard()[0]
        missPlaced=np.sum(current ==self.solution)
        #print(missPlaced)

        goal=[x for row in self.solution for x in row]
        size = len(current)  
        manhattan_distance = 0
        linear_conflict = 0

        # Compute Manhattan distance and Linear Conflict
        for i in range(size):
            missPlaced=np.sum(current !=self.solution)
            #print(missPlaced)
            for j in range(size):
                current_tile = current[i][j]
                if current_tile != 0: # dont process blank space
                    
                    goal_i, goal_j = divmod(goal.index(current_tile), size) # get pos of goal space for given number
                    #print(current_tile)

                    #print(goal_i,goal_j)
                    #print(self.getBoard()[0])
                    # Manhattan distance
                    manhattan_distance += abs(i - goal_i) + abs(j - goal_j)
                    #print(abs(i - goal_i) + abs(j - goal_j))

                   # Check for linear conflicts in the same row
                    if i == goal_i:
                        for k in range(j + 1, size):
                            conflicting_tile = current[i][k]
                            if conflicting_tile != 0 and goal.index(conflicting_tile) // size == i and goal.index(conflicting_tile) < goal.index(current_tile):
                                linear_conflict +=2

                    # Check for linear conflicts in the same column
                    if j == goal_j:
                        for k in range(i + 1, size):
                            conflicting_tile = current[k][j]
                            if conflicting_tile != 0 and goal.index(conflicting_tile) % size == j and goal.index(conflicting_tile) < goal.index(current_tile):
                                linear_conflict += 2

        
        self.heur=(manhattan_distance+linear_conflict+missPlaced) 
    # overload less than operator for use in the priortiy queue // heap ququeu
    def __lt__(self,other):
        # get heuristic values
        self.manhConflict()
        other.manhConflict()
        return self.heur<other.heur
# traversing solution
def printSolutions(endPuzzle,cs,os):
    sol=[endPuzzle]
    # append all parents of end state
    while endPuzzle:
        sol.append(endPuzzle.predecessor)
        endPuzzle=endPuzzle.predecessor
    # count moves
    moveCtr=1
    # print boards
    for brd in sol[::-1]:
        try:
            with open("p1.txt",'a') as txt:
                txt.write(f"MOVE {moveCtr}: "+brd.move)
                print(f"MOVE {moveCtr}: ",brd.move)
                print(brd.getBoard()[0])
                txt.write(np.array2string(brd.getBoard()[0]))
                print(brd.moveCounter)
                txt.write(brd.moveCounter)
            pass
        except:
            pass
        with open("p1.txt",'a') as txt:
            print("-------------------------------------------------------------------------")
            txt.write("-------------------------------------------------------------------------")
        moveCtr+=1
    print("NODES VISITED",len(cs)+len(os))
    print("SOLTUION LENGTH: ",len(sol))
    #print()

def main(puzzle):

    #print(p1[0][2])
    startPuzzle=Puzzled(puzzle,"Initial State",1)
    openSets=[]
    closedSets=[]
    #openSets.extend(tempMoves)
    heapq.heappush(openSets,startPuzzle)
    if startPuzzle.goalReached():
        return False
    else:
        #tempMoves=startPuzzle.genMoves()  
        pass
      

# continuously search until solution found
    while openSets:
        # get best path
        bestOption=heapq.heappop(openSets)
# check if goal
        if bestOption.goalReached():
            #print(bestOption.getBoard())
            # print sol
            return printSolutions(bestOption,openSets,closedSets)

        else:
            # add to closed
            closedSets.append(bestOption.getBoard()[0].flatten())
            newMoves=bestOption.genMoves()
            #exists=np.any(np.all(closedSets))
            for moves in newMoves:
                #print(closedSets)
                exists=np.any(np.all(closedSets==moves.getBoard()[0].flatten(),axis=1))
                if not exists: # in closed set so add to searchable nodes

                        #print(moves.getBoard()[0])
                        heapq.heappush(openSets,moves)
    return False

if __name__ =="__main__":
    p1=np.array([[0,6,2,4],[1,10,3,7],[5,9,14,8],[13,15,11,12]])
    p2=np.array([[9,1,3,4],[5,6,8,7],[13,2,11,12],[14,10,15,0]])
    p3=np.array([[0,12,9,13],[15,11,10,14],[3,7,5,6],[4,8,2,1]])
    pzl=[p1,p2,p3]
    for p in pzl:

        x=main(p)
        if x==False:
            print("NO SOLUTION FOUND")