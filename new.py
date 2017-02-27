import math;
from binaryheap import BinHeap;
from mazeclass import mazeClass


GRID_SIZE = int(101);
grid = [];
path = [];
counter = 0;
index= -1;
grid2=[];

open_states = BinHeap();
closed_states = BinHeap();
expanded_states = 0;

original_start = (0,0);
goal = (0,0);
start = (0,0);

#larger than the largest value that g can have
tie_break_constant = 101*101;
#set infinity to a value that can never be g. i.e. greater than the lengest possible path
infinity = (101*101*100) + 1;

def printGrid():
    for k in range(GRID_SIZE):
        for p in range(GRID_SIZE):
            print( str(grid[k][p].getF() ) + "      "),
        print("");    

    print("-----------------------");

class state:
    def __init__(self, x, y, h):
        self.x = x;
        self.g = infinity;
        self.y = y;
        self.h = h;
        self.f = infinity;
        self.treeX = -1;
        self.treeY = -1;
        self.actions = [(0,1), (1,0), (0,-1), (-1,0)];
        self.action_costs = [1, 1, 1, 1];
        self.search_counter = 0;
        self.blocked = False;

    def setTree(self, co_ords):
        self.treeX = co_ords[0];
        self.treeY = co_ords[1];

    def getTree(self):
        return (self.treeX, self.treeY);    

    def getBlockedStatus(self):
        return self.blocked;

    def setBlocked(self):
        self.blocked = True;

    def increaseActionCosts(self):
        #this state is blocked.. so change all costs that lead to it to infinity
        if (self.x > 0):
            grid[ self.y ][self.x-1].setActionCost(1, infinity); 
        if (self.x < GRID_SIZE-1):
            grid[ self.y ][self.x+1].setActionCost(3, infinity);
        if (self.y > 0):
            grid[ self.y-1 ][self.x].setActionCost(0, infinity); 
        if (self.y < GRID_SIZE-1):
            grid[ self.y+1 ][self.x].setActionCost(2, infinity);         
        
        
    def getActionCost(self, i):
        return self.action_costs[i];

    def setActionCost(self, i, value):
        self.action_costs[i] = value;    

    def getX(self):
        return self.x;

    def getY(self):
        return self.y;

    def getH(self):
        return self.h;

    def setH(self, value):
        self.h = value;

    def setG(self, g):
        self.g = g;

    def setF(self, f, largeG= False, smallG =False):
        if(largeG):
            self.f = (tie_break_constant*f)-self.g;
        elif(smallG):
            self.f = (f+self.g);
        else:    
            self.f = f;    

    def getG(self):
        return self.g;

    def getF(self):
        return self.f;        
    
    def setCounter(self):
        self.search_counter = counter;

    def getCounter(self):
        return self.search_counter;

    def succ(self, i):
        succ_x = self.x + self.actions[i][0];
        succ_y = self.y + self.actions[i][1];
        # check that the new state does not go out of bounds of the grid
        if (succ_x >= GRID_SIZE or succ_y >=GRID_SIZE or succ_y < 0 or succ_x < 0):
            return None;
        else:
            return grid[ succ_y][ succ_x];


#checks if the new state found is already in the Open list
def checkInOpenStates(state):
    global open_states;
    for index,i in enumerate(open_states.heapList):
        if(index == 0):
            continue;
        if ( state.getX() == i.getX() and state.getY() == i.getY() ):
            return index;
    return -1;    


#find path from start to goal using A*
def computePath(goal_local, adaptive=False, largeG = False, smallG = False):

    global expanded_states;
    while ( open_states.currentSize!=0 and grid[ goal_local[1] ][ goal_local[0] ].getG() > open_states.heapList[1].getF() ):
        current_state = open_states.delMin();
        
        expanded_states = expanded_states + 1;
        
        closed_states.insert(current_state);
        
        for i in range(0,4):
            next_s = current_state.succ(i);
            if(next_s == None):
                continue;

            if( next_s.getCounter() < counter ):
                next_s.setG(infinity);
                next_s.setCounter();

            if (next_s.getG() > (current_state.getG() + current_state.getActionCost(i)) ):
                next_s.setG( current_state.getG() + current_state.getActionCost(i) );
                next_s.setF( next_s.getG() + next_s.getH(), largeG, smallG );
                next_s.treeX = current_state.getX();
                next_s.treeY = current_state.getY();
                
                index = checkInOpenStates(next_s);
                if( index == -1 ):
                    open_states.insert(next_s);
                else:
                    # open_states[index] = (next_s.getF(), next_s);
                    # heapq.heapify(open_states);
                    open_states.buildHeap(open_states.heapList[1:len(open_states.heapList)]);


    if(adaptive):
        while( closed_states.currentSize > 0 ):
            current_state = closed_states.delMin();
            current_state.setH( grid[goal_local[1]][goal_local[0]].getG() - current_state.getG() );     

def reset():
    global original_start;
    global goal;
    global start;
    global index;
    global counter;
    global expanded_states;
    global open_states;
    global grid;
    global path;
    global closed_states;

    grid = [];
    path = [];
    counter = 0;
    index = -1;

    open_states = BinHeap();
    closed_states = BinHeap();
    expanded_states = 0;

    start = original_start;


def getMaze():
    global original_start;
    global goal;
    global start;
    global index;
    global grid2;

    m1 = mazeClass();

    example = m1.getMaze();
    
    grid2 = example[0];
    index = example[1];
    original_start = example[2];
    goal = example[3];
    start = original_start;
    

def createGrid(size):
    reset();
    if( len(grid2)==0 ):
        getMaze();

    for j in range(101):
        grid.append([]);
        for i in range(101):
            h = math.fabs(goal[0]-i) + math.fabs(goal[1]-j);
            s = state(i, j, h);
            s.setCounter();
            if(grid2[j][i] == 0):
                s.setBlocked();
            grid[j].append(s);        

def forwardAStar(adaptive = False, largeG = False, smallG = False):

    createGrid(GRID_SIZE);
    global counter;
    global open_states;
    global closed_states;
    # this is maze creation

    while( (goal[0] != start[0]) or (goal[1] != start[1])):
        open_states = BinHeap();
        closed_states = BinHeap();
        counter = counter + 1 ;
        print(start[1], start[0])
        grid[ start[1] ][ start[0] ].setG(0);
        grid[ start[1] ][ start[0] ].setF( 0 + grid[ start[1] ][ start[0] ].getH(), largeG, smallG);
        grid[ start[1] ][ start[0] ].setCounter();

        grid[ goal[1] ][ goal[0] ].setG(infinity);
        grid[ goal[1] ][ goal[0] ].setCounter();

        # obj_for_heap = (grid[ start[1] ][ start[0] ].getF(), grid[ start[1] ][ start[0] ]);
        open_states.insert(grid[ start[1] ][ start[0] ]);
        
        if(largeG):
            computePath(goal,adaptive, True, False);
        elif(smallG):    
            computePath(goal,adaptive, False, True);
        else:
            computePath(goal,adaptive);   

        if( open_states.currentSize == 0 ):
            print "I dont think i can reach the target.";
            break;

        print "Traversing graph";
        traversePath();

    print "Done..";


def traversePath():
    global start;
    global path;

    path = [];
    curr_co_ords = (goal[0], goal[1]);
    path.append( curr_co_ords );
    
    while( curr_co_ords[0] != start[0] or curr_co_ords[1] != start[1] ):
        x = curr_co_ords[0];
        y = curr_co_ords[1];

        curr_co_ords = grid[y][x].getTree();
        path.append(curr_co_ords);

    current = path.pop();
    while(len(path) > 0):

        for i in range(0,4):
            s_local = grid[ current[1] ][ current[0] ].succ(i);
            if(s_local is not None):
                if(s_local.getBlockedStatus()):
                    s_local.increaseActionCosts();

        next = path.pop(); 
        # print(next);         
        if ( grid[next[1]][next[0]].getBlockedStatus() ):
            start = current;
            break;
        else:
            current = next;

    if(len(path)==0):
        start = current;


def backwardAStar(largeG = False):
    createGrid(GRID_SIZE);
    global counter;
    global open_states;
    global closed_states;
    # this is maze creation

    while( (goal[0] != start[0]) or (goal[1] != start[1])):
        open_states = BinHeap();
        closed_states = BinHeap();
        counter = counter + 1 ;
        
        grid[ goal[1] ][ goal[0] ].setG(0);
        grid[ goal[1] ][ goal[0] ].setF( 0 + grid[ goal[1] ][ goal[0] ].getH());
        grid[ goal[1] ][ goal[0] ].setCounter();

        grid[ start[1] ][ start[0] ].setG(infinity);
        grid[ start[1] ][ start[0] ].setCounter();

        # obj_for_heap = (grid[ goal[1] ][ goal[0] ].getF(), grid[ goal[1] ][ goal[0] ]);
        # heapq.heappush( open_states, obj_for_heap);
        open_states.insert(grid[ goal[1] ][ goal[0] ]);
        
        print("computing ..");
        computePath(start, False, largeG, False);

        if( open_states.currentSize == 0 ):
            print "I dont think i can reach the target.";
            break;

        print "Traversing graph";
        traverseBackwardPath();

    print "Done..";


def traverseBackwardPath():
    global start;
    global path;

    path = [];
    current = (start[0], start[1]);
    
    while( current[0] != goal[0] or current[1] != goal[1] ):
        x = current[0];
        y = current[1];

        next = grid[y][x].getTree();
        print(next);    
        for i in range(0,4):
            s_local = grid[ current[1] ][ current[0] ].succ(i);
            if(s_local is not None):
                if(s_local.getBlockedStatus()):
                    s_local.increaseActionCosts();
      
        if ( grid[next[1]][next[0]].getBlockedStatus() ):
            start = current;
            break;
        else:
            current = next;
    start = current;        



# print("1. Backward A star");
# print("2. Forward A star");
# print("3. Adaptive Forward A star");
# print("4. Forward A star with larger g-values breaking ties");
# print("5. Forward A star with smaller g-values breaking ties");

# choice = input("Enter the choice");
# if (choice==1):
#     backwardAStar();
# elif (choice==2):
#     forwardAStar(False, False, False);
# elif (choice==3):
#     forwardAStar(True, False, False);
# elif (choice==4):
#     forwardAStar(False, True, False);
# elif (choice==5):    
#     forwardAStar(False, False, True);

# forwardAStar(False, True, False);
forwardAStar(True, True, False);
pr = expanded_states;

forwardAStar(False, True, False);
pr2 = expanded_states;

print("Expanded states : " + str(pr) + "   "+str(expanded_states));

