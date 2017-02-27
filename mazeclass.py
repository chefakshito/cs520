from random import randint
from PIL import Image

imgx = 500; imgy = 500
image = Image.new("RGB", (imgx, imgy))
pixels = image.load()
color = [(0,0, 0), (255, 255, 255)]

sx=101
sy=101;
nm=50;
maze = [[[0 for x in range(sx)] for y in range(sy)] for z in range(nm)]
dx=[0,1,0,-1]
dy=[-1,0,1,0]
"""
cx=randint(0,mx-1)
cy=randint(0,my-1)
stack.append((cx,cy))
print(stack)
"""
sState=[]
gState=[]

class mazeClass:
    
    def __init__(self):
        global imgx; global imgy;
        global image;
        global pixels;
        global color;

        global sx
        global sy
        
        global maze
        global dx
        global dy

        global nm;
        
        for x in range(nm):
            stack = [(randint(0, sx - 1),randint(0, sy - 1))]
            sState.append(stack[-1])    #The start state is assigned.
            
            while len(stack) > 0:
                (cx, cy) = stack[-1];
                
                maze[x][cy][cx] = 1
                # find a new cell to add
                nlst = [] # list of available neighbors
                
                for i in range(4):
                    ch = randint(0,11)
                    if ch<6:
                        choice=1
                    else: 
                        choice=randint(0,11)
                    nx = cx + dx[i]; ny = cy + dy[i]
                    if nx >= 0 and nx < sx and ny >= 0 and ny < sy:
                        if maze[x][ny][nx] == 0:
        #                    print(maze[x][ny][nx],'check1')     #--CHECK--1--
                            if choice==1:
        #                      print('Entered Choice 1')       #--CHECK--3--
                                # of occupied neighbors must be 1
                                ctr = 0
                                for j in range(4):
                                    ex = nx + dx[j]; ey = ny + dy[j]
                                    if ex >= 0 and ex < sx and ey >= 0 and ey < sy:
                                        if maze[x][ey][ex] == 1: ctr += 1
                                if ctr == 1: nlst.append(i)
                            if choice>1:
         #                       print('Entered Choice 2')       #--CHECK--4--
                                 luck=randint(1,11)
         #                        print(luck,"CHECK 5")          #--CHECK--5--
                                 if luck>choice:
                                     nlst.append(i)
                # if 1 or more neighbors available then randomly select one and move
         #       print(nlst,'check2')     #--CHECK--2--
                if len(nlst) > 0:
                    ir = nlst[randint(0, len(nlst) - 1)]
                    cx += dx[ir]; cy += dy[ir]
                    stack.append((cx, cy))
                else: stack.pop()
            #A random goal state is generated
            while len(gState)!=x+1:
                gx=randint(0,sx-1)
                gy=randint(0,sy-1)
                if maze[x][gx][gy]==1:
                    gState.append((gx,gy))

        
            # # paint the maze
            # for ky in range(imgy):
            #     for kx in range(imgx):
            #         pixels[kx, ky] = color[maze[x][sy * ky // imgy][sx * kx // imgx]]
            # image.save("Maze_" + str(x) + ".png", "PNG")

    def getMaze(self):
        
        c = randint(0,50)
        return (maze[c], c, sState[c], gState[c]);
        