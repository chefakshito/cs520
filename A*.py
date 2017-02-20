from random import randint

open_states = [];
closed_states = [];

class state:
    def __init__(self, x, y, h):
        self.x = x;
        self.y = y;
        self.h = h;
        self.actions = [(0,1), (1,0), (0,-1), (-1,0)];
    
    def setG(self, g):
        self.g = g;
        self.f = self.g + self.h;
    
    def succ(self, i):
        return grid[ self.x + self.actions[i][0], self.y + self.actions[i][1] ];


while goal.g > heap_pop_without_removing:
    next_state = heap_pop;
    heappush( closed_states, next_state );
    
    for i in range(0,4):
        next_state.succ(i);
        
