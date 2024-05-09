import pygame,ast,math

import ctypes
ctypes.windll.user32.SetProcessDPIAware()

screen = pygame.display.set_mode((0,0),pygame.FULLSCREEN)
clock = pygame.time.Clock()

def checkExit():
    key = pygame.key.get_pressed()
    for event in pygame.event.get():
        if event.type == pygame.QUIT or key[pygame.K_ESCAPE]:
            file = open(path,"w")
            file.write(f'{[balls,links,linkLength,linkStrength]}')
            pygame.quit()
            exit()

def getDist(p1,p2):
    return math.sqrt(((p1[0]-p2[0])**2)+((p1[1]-p2[1])**2))

path = "Info.txt"
file = open(path,"r")
file = ast.literal_eval(file.read())
print(file)

clicked = False
clicked2 = False
clicked3 = False

selected = 0
c = False

balls,links,linkLength,linkStrength = file

r = 20
r2 = 60

springStrength = 100

bounds = screen.get_size()

while True:
    checkExit()
    screen.fill((20,20,20))
    
    for i in range(bounds[0]//r):
        pygame.draw.line(screen,(50,50,50),(i*r,0),(i*r,bounds[1]))
    for i in range(bounds[1]//r):
        pygame.draw.line(screen,(50,50,50),(0,i*r),(bounds[0],i*r))
    for i in range(bounds[0]//(r2)):
        pygame.draw.line(screen,(50,50,50),(i*r2,0),(i*r2,bounds[1]),3)
    for i in range(bounds[1]//(r2)):
        pygame.draw.line(screen,(50,50,50),(0,i*r2),(bounds[0],i*r2),3)
    
    key = pygame.key.get_pressed()
    mousePos = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()
    if click[0]:
        if not clicked:
            clicked = True
            balls.append([round(mousePos[0]/r)*r,round(mousePos[1]/r)*r])
    elif key[pygame.K_m]:
                if not clicked:
                    clicked = True
                    if c:
                        c = False
                        balls[selected] = [round(mousePos[0]/r)*r,round(mousePos[1]/r)*r]
                        for k in range(len(links)):
                                if selected in links[k]:
                                    linkLength[k] = getDist(balls[links[k][0]],balls[links[k][1]])
                                    print(linkLength[k])
                        print("Ball moved")
    else:
        clicked = False
    
    if key[pygame.K_z]:
        if not clicked3:
            clicked3 = True
            springStrength += 50
            if springStrength >= 200:
                springStrength = 50
            print('Spring damping:',springStrength)
    else:
        clicked3 = False
    
    
    if key[pygame.K_y] and key[pygame.K_u]:
        balls,links,linkLength,linkStrength = [[],[],[],[]]
    i = -1
    for _ in range(len(balls)):
        i += 1
        dist = getDist(balls[i],mousePos)
        if dist < 20:
            if click[2]:
                del balls[i]
                #delete links with deleted ball
                k = -1
                for _ in range(len(links)):
                    k += 1
                    if i in links[k]:
                        del links[k]
                        del linkLength[k]
                        k -= 1
                #move all link indexes
                for k in range(len(links)):
                    if links[k][0] > i:
                        links[k][0] -= 1
                    if links[k][1] > i:
                        links[k][1] -= 1
                i -= 1
                continue
            if key[pygame.K_SPACE]:
                if not clicked2:
                    clicked2 = True
                    if c:
                        if i != selected:
                            #if not any([(selected in links[i] and i in links[i]) for i in range(len(links))]):
                                c = False
                                links.append(sorted([selected,i]))
                                linkLength.append(getDist(balls[selected],balls[i]))
                                linkStrength.append(springStrength)
                                print(selected,i)
                                print(linkLength[-1])
                                print("Added link")
                    else:
                        c = True
                        selected = i
                        print("Select another ball")
            elif key[pygame.K_d]:
                if not clicked2:
                    clicked2 = True
                    if c:
                        if i != selected:
                            c = False
                            for k in range(len(links)):
                                if selected in links[k] and i in links[k]:
                                    del links[k]
                                    del linkLength[k]
                                    del linkStrength[k]
                                    break
                            print("Link deleted")
            elif key[pygame.K_s]:
                if not clicked2:
                    clicked2 = True
                    if c:
                        if i != selected:
                            c = False
                            for k in range(len(links)):
                                if selected in links[k] and i in links[k]:
                                    linkStrength[k] += 50
                                    if linkStrength[k] >= 200:
                                        linkStrength[k] = 50
                                    break
                            print("Link strength changed")
            else:
                clicked2 = False
    
    for i in range(len(balls)):
        pygame.draw.circle(screen,(255,255,255),balls[i],20)
    
    for i in range(len(links)):
        if links[i][0] < len(balls) and links[i][1] < len(balls):
            pygame.draw.line(screen,((linkStrength[i]-100)*2+100,150,0),balls[links[i][0]],balls[links[i][1]],2)
    
    pygame.display.update()
    clock.tick(60)