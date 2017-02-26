import math;
import heapq;


GRID_SIZE = int(10);
grid = [];
path = [];
counter = 0;

open_states = [];
closed_states = [];

original_start = (0,2);
goal = (9,8);
start = original_start;

#set infinity to a value that can never be g. i.e. greater than the lengest possible path
infinity = (101*101) + 1;


class state:
    def __init__(self, x, y, h):
        self.x = x;
        self.g = 0;
        self.y = y;
        self.h = h;
        self.f = 0;
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
            grid[ self.x-1 ][self.y].setActionCost(1, infinity); 
        if (self.x < GRID_SIZE-1):
            grid[ self.x+1 ][self.y].setActionCost(3, infinity);
        if (self.y > 0):
            grid[ self.x ][self.y-1].setActionCost(0, infinity); 
        if (self.y < GRID_SIZE-1):
            grid[ self.x ][self.y+1].setActionCost(2, infinity);         
        
        
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
            return grid[ succ_x][ succ_y];


#checks if the new state found is already in the Open list
def checkInOpenStates(state):
    global open_states;
    for index,i in enumerate(open_states):
        if ( state.getX() == i[1].getX() and state.getY() == i[1].getY() ):
            return index;
    return -1;    


#find path from start to goal using A*
def computePath():
    
    while ( len(open_states)!=0 and grid[ goal[0] ][ goal[1] ].getG() > heapq.nsmallest(1, open_states)[0][1].getF() ):
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

        

def createGrid(size):
    for j in range(size):
        grid.append([]);
        for i in range(size):
            h = math.fabs(goal[0]-i) + math.fabs(goal[1]-j);
            s = state(i, j, h);
            s.setCounter();
            grid[j].append(s);
        

def main():
    createGrid(GRID_SIZE);
    global counter;
    global open_states;
    global closed_states;
    # this is maze creation

    while( (goal[0] != start[0]) or (goal[1] != start[1])):
        open_states = [];
        closed_states = [];
        counter = counter + 1 ;
        grid[ start[0] ][ start[1] ].setG(0);
        grid[ start[0] ][ start[1] ].setF( 0 + grid[ start[0] ][ start[1] ].getH());
        grid[ start[0] ][ start[1] ].setCounter();

        grid[ goal[0] ][ goal[1] ].setG(infinity);
        grid[ goal[0] ][ goal[1] ].setCounter();

        obj_for_heap = (grid[ start[0] ][ start[1] ].getF(), grid[ start[0] ][ start[1] ]);
        heapq.heappush( open_states, obj_for_heap);
        
        computePath();

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
    i = 0;
    while( curr_co_ords[0] != start[0] or curr_co_ords[1] != start[1] ):
        x = curr_co_ords[0];
        y = curr_co_ords[1];

        curr_co_ords = grid[x][y].getTree();
        path.append(curr_co_ords);

    current = path.pop();
    while(len(path) > 0):

        for i in range(0,4):
            s_local = grid[ current[0] ][ current[1] ].succ(i);
            if(s_local is not None):
                if(s_local.getBlockedStatus()):
                    s_local.increaseActionCosts();

        next = path.pop();            
        if ( next.getBlockedStatus() ):
            start = current;
            break;
        else:
            current = next;


# call the program
main();