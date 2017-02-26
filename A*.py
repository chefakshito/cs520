import math;
import heapq;

#***** MAKE SURE THAT EVERYTIME f IS CHANGED, HEAPIFY IS CALLED TO SORT
#use actual tree to mark the path and then recreate the path to traverse

grid = [];
path = [];

original_start = (0,2);
goal = (9,8);
start = original_start;

#set infinity to a value that can never be g. i.e. greater than the lengest possible path
infinity = (101*101) + 1;


class state:
    def __init__(self, x, y, h):
        self.x = x;
        self.y = y;
        self.h = h;
        self.actions = [(0,1), (1,0), (0,-1), (-1,0)];
        action_costs = [1, 1, 1, 1];
        self.search_counter = 0;
        self.blocked = False;

    def getBlockedStatus(self):
        return self.blocked;

    def setBlocked(self):
        self.blocked = True;

    def increaseActionCost(self, i):
        self.action_costs[i] = infinity;
        
    def getActionCost(self, i):
        return self.action_costs[i];

    def getX(self):
        return self.x;

    def getY(self):
        return self.y;

    def setG(self, g):
        self.g = g;
        self.f = self.g + self.h;

    def getG(self):
        return self.g;

    def getF(self):
        return self.f;        
    
    def setCounter(self):
        self.search_counter = counter;

    def getCounter(self):
        return self.search_counter;

    def succ(self, i):
        #check if its not a boundary
        return grid[ self.x + self.actions[i][0], self.y + self.actions[i][1] ];


def computePath():
    #Are we assuming that this algo will stop if it has encountered a blocked cell?
    path = [];
    while ( grid[ goal[0] ][ goal[1] ].getG() > heapq.nsmallest(1, open_states)[0][1].getF() ):
        current_state = heapq.heappop(open_states)[1];

        obj_for_heap = (current_state.getF(), current_state);
        heappush( closed_states, obj_for_heap );
        
        for i in range(0,4):
            next_s = current_state.succ(i);
            if(next_s == null):
                continue;

            if( next_s.getCounter() < counter ):
                next_s.setG(infinity);
                next_s.setCounter();

            if next_s.getG() > (current_state.getG() + current_state.getActionCost(i)):
                next_s.setG( current_state.getG() + current_state.getActionCost(i) );
                path.append(next_s);
                
                obj_for_heap = (next_s.getF(), next_s);
                heappush( open_states, obj_for_heap);
            
        
def main():
    counter = 0;

    # this is maze creation
    def createGrid(grid, size):
        for j in size:
            grid.append([]);
            for i in size:
                h = math.abs(goal[0]-i) + math.abs(goal[1]-j);
                s = state(i, j, h);
                s.setCounter(0);
                grid[i].append(s);


    while(goal != start):
        counter = counter + 1 ;
        grid[ start[0] ][ start[1] ].setG(0);
        grid[ start[0] ][ start[1] ].setCounter(counter);

        grid[ goal[0] ][ goal[1] ].setG(infinty);
        grid[ goal[0] ][ goal[1] ].setCounter(counter);

        open_states = [];
        closed_states = [];

        obj_for_heap = (grid[ start[0] ][ start[1] ].getF(), grid[ start[0] ][ start[1] ]);
        heappush( open_states, obj_for_heap);
        
        computePath();

        if( len(open_states) == 0 ):
            print "I dont think i can reach the target.";
            break;

        traversePath();
        #update path costs if a blockage was found
        if (goal != start):
            for i in range(0,4):
                s_local = start.succ(i);
                if(s_local != null):
                    if(s_local.getBlockedStatus()):
                        s_local.increaseActionCost(i);


        
print "Yess.. yahi mei chahtaa tha..";

def traversePath():
    for s in path:
        if( (s.getX() == goal[0]) && (s.getY() == goal[1]) ):
            break;

        getout = False;    
        for i in range(4):
            if (s.getActionCost[i] > 1):
                getout = True;
        if(getout):
            break;                
    
    start[0] = s.getX();
    start[1] = s.getY();