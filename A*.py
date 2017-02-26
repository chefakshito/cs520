import math;
import heapq;


GRID_SIZE = int(20);
grid = [];
path = [];
counter = 0;

open_states = [];
closed_states = [];

original_start = (1,1);
goal = (16,10);
start = original_start;

#set infinity to a value that can never be g. i.e. greater than the lengest possible path
infinity = (101*101) + 1;

def printGrid():
    for k in range(GRID_SIZE):
        for p in range(GRID_SIZE):
            print( str(grid[k][p].getG() ) + "      "),
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

    def setF(self, f):
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
    for index,i in enumerate(open_states):
        if ( state.getX() == i[1].getX() and state.getY() == i[1].getY() ):
            return index;
    return -1;    


#find path from start to goal using A*
def computePath(goal_local, adaptive=False):
    
    while ( len(open_states)!=0 and grid[ goal_local[1] ][ goal_local[0] ].getG() > heapq.nsmallest(1, open_states)[0][1].getF() ):
        current_state = heapq.heappop(open_states)[1];

        obj_for_heap = (current_state.getF(), current_state);
        heapq.heappush( closed_states, obj_for_heap );
        
        for i in range(0,4):
            next_s = current_state.succ(i);
            if(next_s == None):
                continue;

            if( next_s.getCounter() < counter ):
                next_s.setG(infinity);
                next_s.setCounter();

            if (next_s.getG() > (current_state.getG() + current_state.getActionCost(i)) ):
                next_s.setG( current_state.getG() + current_state.getActionCost(i) );
                next_s.setF( next_s.getG() + next_s.getH() );
                next_s.treeX = current_state.getX();
                next_s.treeY = current_state.getY();
                
                index = checkInOpenStates(next_s);
                if( index == -1 ):
                    obj_for_heap = (next_s.getF(), next_s);
                    heapq.heappush( open_states, obj_for_heap);
                else:
                    open_states[index] = (next_s.getF(), next_s);
                    heapq.heapify(open_states);    

    if(adaptive):
        while( len(closed_states) > 0 ):
            current_state = heapq.heappop(closed_states)[1];
            current_state.setH( grid[goal_local[1]][goal_local[0]].getG() - current_state.getG() );     


def createGrid(size):
    for j in range(size):
        grid.append([]);
        for i in range(size):
            h = math.fabs(goal[0]-i) + math.fabs(goal[1]-j);
            s = state(i, j, h);
            s.setCounter();
            grid[j].append(s);
    grid[8][14].setBlocked();
    grid[6][14].setBlocked();
    grid[6][14].setBlocked();
    grid[7][13].setBlocked();
    grid[12][4].setBlocked();
    grid[11][4].setBlocked();
    grid[10][4].setBlocked();        
        

def forwardAStar(adaptive = False):

    createGrid(GRID_SIZE);
    global counter;
    global open_states;
    global closed_states;
    # this is maze creation

    ter = 0;
    while( (goal[0] != start[0]) or (goal[1] != start[1])):
        open_states = [];
        closed_states = [];
        counter = counter + 1 ;
        
        grid[ start[1] ][ start[0] ].setG(0);
        grid[ start[1] ][ start[0] ].setF( 0 + grid[ start[1] ][ start[0] ].getH());
        grid[ start[1] ][ start[0] ].setCounter();

        grid[ goal[1] ][ goal[0] ].setG(infinity);
        grid[ goal[1] ][ goal[0] ].setCounter();

        obj_for_heap = (grid[ start[1] ][ start[0] ].getF(), grid[ start[1] ][ start[0] ]);
        heapq.heappush( open_states, obj_for_heap);
        
        computePath(goal,adaptive);

        if( len(open_states) == 0 ):
            print "I dont think i can reach the target.";
            break;

        print "Traversing graph";
        traversePath();

    print "Yess.. yahi mei chahtaa tha..";


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
        print(next);         
        if ( grid[next[1]][next[0]].getBlockedStatus() ):
            start = current;
            break;
        else:
            current = next;

    if(len(path)==0):
        start = current;


def backwardAStar():
    createGrid(GRID_SIZE);
    global counter;
    global open_states;
    global closed_states;
    # this is maze creation

    while( (goal[0] != start[0]) or (goal[1] != start[1])):
        open_states = [];
        closed_states = [];
        counter = counter + 1 ;
        
        grid[ goal[1] ][ goal[0] ].setG(0);
        grid[ goal[1] ][ goal[0] ].setF( 0 + grid[ goal[1] ][ goal[0] ].getH());
        grid[ goal[1] ][ goal[0] ].setCounter();

        grid[ start[1] ][ start[0] ].setG(infinity);
        grid[ start[1] ][ start[0] ].setCounter();

        obj_for_heap = (grid[ goal[1] ][ goal[0] ].getF(), grid[ goal[1] ][ goal[0] ]);
        heapq.heappush( open_states, obj_for_heap);
        
        print("computing ..");
        computePath(start);

        if( len(open_states) == 0 ):
            print "I dont think i can reach the target.";
            break;

        print "Traversing graph";
        traverseBackwardPath();

    print "Yess.. yahi mei chahtaa tha..";


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


# call the program
forwardAStar(True);