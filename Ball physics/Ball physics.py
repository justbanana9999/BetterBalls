import pygame,random,copy,math,ast

import ctypes
ctypes.windll.user32.SetProcessDPIAware()
pygame.init()
screen = pygame.display.set_mode((0,0),pygame.FULLSCREEN,pygame.HWSURFACE)
clock = pygame.time.Clock()



def checkExit():
    key = pygame.key.get_pressed() 
    if key[pygame.K_ESCAPE]:
        pygame.quit()
        exit()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

def addBall(pos):
    ballVel.append([0,0])
    ballPos.append(list(pos))
    #ballColor.append(colorsys.hsv_to_rgb(random.random(),1,1))
    #ballColor[-1] = (ballColor[-1][0]*255,ballColor[-1][1]*255,ballColor[-1][2]*255)
    #ballSize.append(random.randint(20,30))
    ballColor.append((255,255,255))
    ballSize.append(20)

def resetBalls(amount):
    global ballPos,ballVel,ballColor,ballSize,oldPos
    ballPos = []
    ballVel = []
    ballColor = []
    ballSize = []
    for i in range(amount):
        if i < len(startPos):
            addBall(startPos[i])
        else:
            addBall([random.randint(300-100,300+100),random.randint(300-100,300+100)])

def pointAt(p1,p2):
    dx = p1[0]-p2[0]
    dy = p1[1]-p2[1]

    if dy == 0:
        if dx < 0:
            d = -90
        else:
            d = 90
    else:
        if dy < 0:
            d = 180+math.degrees(math.atan(dx/dy))
        else:
            d = math.degrees(math.atan(dx/dy))
    return math.radians(d)

try:
    path = "Info.txt"
    file = open(path,"r")
    file = ast.literal_eval(file.read())
    print(file)

    startPos,links,linkDist,damping = file
except:
    startPos,links,linkDist,damping = [],[],[],[]

balls = len(startPos)
ballPos,ballVel,ballColor,ballSize = [],[],[],[]
resetBalls(balls)

force = 0.5
iterations = 10
dist = 100
mouseRange = 50

selectedBall = 0

clicked = False
clicked2 = False

bounds = screen.get_size()
clock = pygame.time.Clock()
font = pygame.font.Font('freesansbold.ttf', 32)
minfps = 25
status = ["",[0,128,0]]

while True:
    checkExit()
    

    screen.fill((20,20,20))
   
    mouseClick = pygame.mouse.get_pressed()
    mousePos = pygame.mouse.get_pos()
    fps = clock.get_fps()
    
    if fps > minfps:
        status = ["Good",[0,128,0]]
    else:
        status = ["Bad",[128,0,0]]
    
    
    text = font.render(status[0], False, status[1])
    
    if mouseClick[0] and not fps < minfps:
        balls += 1
        addBall(mousePos)
    key = pygame.key.get_pressed()
    if key[pygame.K_SPACE]:
        if not clicked:
            clicked = True
            balls += 1
            addBall(mousePos)
    else:
        clicked = False

    oldPos = copy.deepcopy(ballPos)

    #move balls
    i = -1
    for _ in range(balls):
        i += 1

        if abs(ballVel[i][0]) <= 0.1:
            ballVel[i][0] = 0
        if abs(ballVel[i][1]) <= 0.1:
            ballVel[i][1] = 0
        
        ballPos[i][0] += ballVel[i][0]
        ballPos[i][1] += ballVel[i][1]
        
        if mouseClick[2]:
            dist = math.dist(ballPos[i],mousePos)
            if dist < mouseRange:
                balls -= 1
                
                del ballPos[i]
                del ballVel[i]
                del ballColor[i]
                del oldPos[i]
                del ballSize[i]
                i -= 1
                if balls == 0:
                    break
                continue
        if mouseClick[1] or key[pygame.K_c]:
            dist = math.dist(ballPos[i],mousePos)
            minDist = ballSize[i]
            if dist < minDist:
                if not clicked2:
                    clicked2 = True
                    selectedBall = i
            if selectedBall != -1:
                ballPos[selectedBall] = list(mousePos)
        else:
            clicked2 = False
            selectedBall = -1
        
        #physics and collision
        for _ in range(iterations):
            for j in range(balls):
                if j == i:
                    continue
                
                #check if link
                link = False
                for _ in range(len(links)):
                    if (links[_][0] == i and links[_][1] == j) or (links[_][0] == j and links[_][1] == i):
                        selectedLink = _
                        minDist = linkDist[selectedLink]
                        link = True
                        break
                if not link:
                    minDist = ballSize[i]+ballSize[j]
                
                if link:
                    dist = math.dist(ballPos[i],ballPos[j])
                    direction = pointAt(ballPos[i],ballPos[j])

                    move = [math.sin(direction)*(dist-minDist)/(damping[selectedLink]*iterations/5),
                            math.cos(direction)*(dist-minDist)/(damping[selectedLink]*iterations/5)]
                    
                    ballPos[i][0] -= move[0]
                    ballPos[i][1] -= move[1]
                    ballPos[j][0] += move[0]
                    ballPos[j][1] += move[1]
                else:
                    squareDist = [ballPos[i][0]-ballPos[j][0],ballPos[i][1]-ballPos[j][1]]
                    if abs(squareDist[0]) < 40 or abs(squareDist[1]) < 40:
                        dist = math.dist(ballPos[i],ballPos[j])
                        if dist < minDist:
                            direction = pointAt(ballPos[i],ballPos[j])
                            
                            move = [math.sin(direction)*(dist-minDist)/(iterations*2),
                                    math.cos(direction)*(dist-minDist)/(iterations*2)]
                            
                            ballPos[i][0] -= move[0]
                            ballPos[i][1] -= move[1]
                            ballPos[j][0] += move[0]
                            ballPos[j][1] += move[1]
        
        ballPos[i][1] += force
        
        #constrain balls by bounds
        if ballPos[i][1] < ballSize[i]:
            ballPos[i][1] = ballSize[i]
        if ballPos[i][1] > bounds[1]-ballSize[i]:
            ballPos[i][1] = bounds[1]-ballSize[i]
        if ballPos[i][0] > bounds[0]-ballSize[i]:
            ballPos[i][0] = bounds[0]-ballSize[i]
        if ballPos[i][0] < ballSize[i]:
            ballPos[i][0] = ballSize[i]
        
        #set vel
        ballVel[i][0] = ballPos[i][0]-oldPos[i][0]
        ballVel[i][1] = ballPos[i][1]-oldPos[i][1]

    #draw mouse range
    if mouseClick[1] or key[pygame.K_c]:
        pygame.draw.circle(screen,(100,100,0),mousePos,mouseRange)
    if mouseClick[2]:
        pygame.draw.circle(screen,(100,0,0),mousePos,mouseRange)

    #draw ball links
    for i in range(len(links)):
        if links[i][0] < balls and links[i][1] < balls:
            pygame.draw.line(screen,(255,0,0),ballPos[links[i][0]],ballPos[links[i][1]],2)
    
    #draw balls
    for i in range(balls):
        pygame.draw.circle(screen,(ballColor[i]),ballPos[i],ballSize[i])
        
    screen.blit(text, (0,0))

    pygame.display.update()
    clock.tick(60)
