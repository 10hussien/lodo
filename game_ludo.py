import pygame
import random
from pygame.locals import *
import sys
from pygame import font
import time

class gridObj:
    def __init__(self, bgColor, playerList, safe, coordinate):
        self.bgColor = bgColor
        self.playerList = playerList
        self.safe = safe
        self.coordinate = coordinate


class Token:
    def __init__(self, Id, color, state, coordinate,size):
        self.Id = Id
        self.color = color
        self.state = state
        self.coordinate = coordinate
        self.size=size
        self.original_coordinate = coordinate


cList = [(1, 6), (2, 6), (3, 6), (4, 6), (5, 6), (6, 5), (6, 4), (6, 3), (6, 2), (6, 1), (6, 0), (7, 0), (8, 0), (8, 1),
        (8, 2), (8, 3), (8, 4), (8, 5), (9, 6), (10, 6), (11, 6), (12, 6), (13, 6), (14, 6), (14, 7),(14, 8), (13, 8),
        (12, 8), (11, 8), (10, 8), (9, 8), (8, 9), (8, 10), (8, 11), (8, 12), (8, 13), (8, 14), (7, 14),(6, 14), (6, 13),
        (6, 12), (6, 11), (6, 10), (6, 9), (5, 8), (4, 8), (3, 8), (2, 8), (1, 8), (0, 8), (0, 7),(0, 6)]
#RGBY
initPos=[[[1,1],[1,4],[4,1],[4,4]],[[10,1],[13,1],[10,4],[13,4]],[[1,10],[4,10],[1,13],[4,13]],[[10,10],[10,13],[13,10],[13,13]]]
pnames=['R','G','B','Y']

height = 1000
width = 800
initx = 0
inity = 0
currentPlayer = 'R'
compTokensLoc=[[1,1],[1,4],[4,1],[4,4]]
n=2
withComputer=False
dice_clicked = False
move_list = []
diceValue = 6


Game_grid = [[-1 for _ in range(15)] for _ in range(15)]
colors=['white','red','green','yellow','blue','black']
colorMatrix = [[-1, -1, -1, -1, -1, -1, 0, 0, 0, -1, -1, -1, -1, -1, -1],
                [-1, -1, -1, -1, -1, -1, 0, 2, 2, -1, -1, -1, -1, -1, -1],
                [-1, -1, -1, -1, -1, -1, 2, 2, 0, -1, -1, -1, -1, -1, -1],
                [-1, -1, -1, -1, -1, -1, 0, 2, 0, -1, -1, -1, -1, -1, -1],
                [-1, -1, -1, -1, -1, -1, 0, 2, 0, -1, -1, -1, -1, -1, -1],
                [-1, -1, -1, -1, -1, -1, 0, 2, 0, -1, -1, -1, -1, -1, -1],
                [0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 4, 0, 0],
                [0, 1, 1, 1, 1, 1, 0, 5, 0, 4, 4, 4, 4, 4, 0],
                [0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 4, 0],
                [-1, -1, -1, -1, -1, -1, 0, 3, 0, -1, -1, -1, -1, -1, -1],
                [-1, -1, -1, -1, -1, -1, 0, 3, 0, -1, -1, -1, -1, -1, -1],
                [-1, -1, -1, -1, -1, -1, 0, 3, 0, -1, -1, -1, -1, -1, -1],
                [-1, -1, -1, -1, -1, -1, 0, 3, 3, -1, -1, -1, -1, -1, -1],
                [-1, -1, -1, -1, -1, -1, 3, 3, 0, -1, -1, -1, -1, -1, -1],
                [-1, -1, -1, -1, -1, -1, 0, 0, 0, -1, -1, -1, -1, -1, -1]]
coordinateMatrix = [[[initx + i * 50, inity + j * 50] for i in range(0, 15)] for j in range(0, 15)]
safeLocs=[[6,2],[8,1],[12,6],[13,8],[8,12],[6,13],[2,8],[1,6]]
safeMatrix = [[0 for i in range(15)] for j in range(15)]

for i in safeLocs:
    safeMatrix[i[0]][i[1]] = 1

diceFaces = {1: [[0, 0, 0], [0, 1, 0], [0, 0, 0]],
        2: [[0, 1, 0], [0, 0, 0], [0, 1, 0]],
        3: [[0, 1, 0], [0, 1, 0], [0, 1, 0]],
        4: [[1, 0, 1], [0, 0, 0], [1, 0, 1]],
        5: [[1, 0, 1], [0, 1, 0], [1, 0, 1]],
        6: [[1, 0, 1], [1, 0, 1], [1, 0, 1]],
            }

for i in range(15):
    for j in range(15):
        ob = gridObj(colors[colorMatrix[i][j]], [], safeMatrix[i][j], coordinateMatrix[i][j])
        Game_grid[i][j] = ob

for j in range(4):
    for i in range(1,5):
        p=initPos[j][i-1]
        R= Token(pnames[j]+str(i), colors[j+1], 0, (50 *p[0] , 50 * p[1]), 20)
        Game_grid[p[0]][p[1]].playerList.append(R)

def drawGrid():
    global Game_grid
    newSurface = pygame.display.set_mode((height, width))
    newSurface.fill('bisque')
    for i in range(15):
        for j in range(15):
            pygame.draw.rect(newSurface, Game_grid[i][j].bgColor, tuple(Game_grid[i][j].coordinate + [50, 50]))
            pygame.draw.rect(newSurface, (0, 0, 0), tuple(Game_grid[i][j].coordinate + [50, 50]), 1)

    # always constant
    pygame.draw.rect(newSurface, colors[1], (initx, inity, 300, 300))
    pygame.draw.rect(newSurface, colors[0], (initx + 50, inity + 50, 200, 200))
    pygame.draw.rect(newSurface, colors[2], (initx + 450, inity, 300, 300))
    pygame.draw.rect(newSurface, colors[0], (initx + 500, inity + 50, 200, 200))
    pygame.draw.rect(newSurface, colors[3], (initx, inity + 450, 300, 300))
    pygame.draw.rect(newSurface, colors[0], (initx + 50, inity + 500, 200, 200))
    pygame.draw.rect(newSurface, colors[4], (initx + 450, inity + 450, 300, 300))
    pygame.draw.rect(newSurface, colors[0], (initx + 500, inity + 500, 200, 200))

    for i in range(15):
        for j in range(15):
            relativeToken(Game_grid[i][j].playerList, i * 50, j * 50)
            for k in Game_grid[i][j].playerList:
                c = k.coordinates
                pygame.draw.circle(newSurface, k.color, (c[0] + 25, c[1] + 25), k.size)
                pygame.draw.circle(newSurface, colors[-1], (c[0] + 25, c[1] + 25), k.size, 1)
                # highlight
                if k.Id[0] == currentPlayer:
                    pygame.draw.circle(newSurface, colors[0], (c[0] + 25, c[1] + 25), k.size - 2, 2)
    # chess_faces

    face = diceFaces[diceValue]
    for i in range(3):
        for j in range(3):
            pygame.draw.rect(newSurface, 'black', ((0 + 800) + (50 * j), (0 + 300) + (50 * i), 50, 50))
            if face[i][j] == 1:
                cIndex=pnames.index(currentPlayer)+1
                pygame.draw.circle(newSurface, colors[cIndex], ((0 + 800) + (50 * j) + 25, (0 + 300) + (50 * i) + 25),
                                10)
    pygame.draw.rect(newSurface, colors[pnames.index(currentPlayer)+1], ((0 + 798), (0 + 298), 150, 150), 4)
    return newSurface

def move(initPos, value, current):
    i = 0
    j = -1
    flag = 0
    while True:
        if cList[i] == initPos or j >= 0:
            if current == 'R' and i == 50:
                flag = 1
            if current == 'G' and i == 11:
                flag = 2
            if current == 'B' and i == 37:
                flag = 3
            if current == 'Y' and i == 24:
                flag = 4
            j += 1
            if j == value:
                break
        i = (i + 1) % len(cList)
    if flag == 1:
        return (cList[i][0] + 1, cList[i][1] + 1)
    elif flag == 2:
        return (cList[i][0] + 1, cList[i][1] + 1)
    elif flag == 3:
        return (cList[i][0] + 1, cList[i][1] - 1)
    elif flag == 4:
        return (cList[i][0] - 1, cList[i][1] - 1)
    else:
        return (cList[i][0], cList[i][1])


def relativeToken(pList, x, y):
    l = len(pList)
    relRad = int((2 / (l + 1)) * 20)
    relpt = []
    j = 0
    if l % 2 == 0:
        l1 = [i + 1 for i in range((l // 2))]
        l2 = [i - 1 for i in range((l // 2))]
        relpt = l2[::-1] + l1
    else:
        l1 = [i + 1 for i in range((l // 2))]
        l2 = [i - 1 for i in range((l // 2))]
        relpt = l2[::-1] + [0] + l1
    for p in pList:
        p.size = relRad
        p.coordinates = ((x) + (relpt[j] * (relRad // 2)), (y))
        j += 1

def check(pos):
    if pos in cList:
        return True
    else:
        return False
    
def gridlocation(pos):
    x = pos[0]
    y = pos[1]
    return (x // 50, y // 50)

        
def checkCollision(pList):
    global currentPlayer
    global Game_grid
    new_list=[]
    for p in pList:
        if p.Id[0] == currentPlayer:
            new_list.append(p)
        else:
            p.coordinates=p.original_coordinate
            i=p.coordinates[0]//50
            j=p.coordinates[1]//50
            Game_grid[i][j].playerList.append(p)
    return new_list

def checkId(pList):
    global currentPlayer
    for i in pList:
        if i.Id[0] == currentPlayer:
            return True
    return False

def compLoc(diceValue):
    global compTokensLoc
    saveLocs=[(1, 7),(2, 7),(3, 7),(4, 7),(5, 7),(6, 7),(7, 7)]
    inits=[]
    players=[]
    if(compTokensLoc[0]==[1,1]):
        inits.append(0)
    else:
        players.append(0)
    if(compTokensLoc[1]==[1,4]):
        inits.append(1)
    else:
        players.append(1)
    if(compTokensLoc[2]==[4,1]):
        inits.append(2)
    else:
        players.append(2)
    if(compTokensLoc[3]==[4,4]):
        inits.append(3)
    else:
        players.append(3)
    if(diceValue==6 and len(inits)>0):
        tkn=random.randint(1,len(inits))
        compTokensLoc[tkn-1]=cList[0]
        return compTokensLoc[tkn-1]
    cnt=len(compTokensLoc)-len(inits)
    print(inits)
    if(cnt<=0):
        return (1,1)
    if(cnt>0):
        
        tkn=random.randint(1,cnt)
        tkn=players[tkn-1]
        print(tkn)
        ind=cList.index(compTokensLoc[tkn])
        if(compTokensLoc[tkn] in saveLocs):
            ind=saveLocs.index(compTokensLoc[tkn])
            if((ind+diceValue) <=(len(saveLocs-1))):
                compTokensLoc[tkn]=saveLocs[ind+diceValue]
                return compTokensLoc[tkn]
            else:
                compLoc(diceValue)
        elif(ind+diceValue<len(cList)-1):
            compTokensLoc[tkn]=cList[ind+diceValue]

        else:
            stepsLeft= diceValue-(len(cList)-1)
            compTokensLoc[tkn]=saveLocs[stepsLeft-1]
        return compTokensLoc[tkn] 

def nextPlayer():
    global n,currentPlayer
    if(n==2):
        if currentPlayer == 'R':
            currentPlayer = 'B'
        elif currentPlayer == 'B':
            currentPlayer = 'R'
    elif(n==3):
        if currentPlayer == 'R':
            currentPlayer = 'G'
        elif currentPlayer == 'G':
            currentPlayer = 'Y'
        elif currentPlayer == 'Y':
            currentPlayer = 'R'
    elif(n==4):
        if currentPlayer == 'R':
            currentPlayer = 'G'
        elif currentPlayer == 'G':
            currentPlayer = 'Y'
        elif currentPlayer == 'Y':
            currentPlayer = 'R'
        elif currentPlayer == 'B':
            currentPlayer = 'R'

global DISPLAYSURF

def mainGame():
    height = 1000
    width = 800
    pygame.init()
    DISPLAYSURF = pygame.display.set_mode((height, width))
    pygame.display.set_caption('PythonGeeks Ludo Game')
    global cList, initPos,pnames,initx,inity,currentPlayer,n,dice_clicked,move_list,diceValue,Game_grid,colors,colorMatrix, coordinateMatrix,safeMatrix,safeLocs,diceFaces
    

    font = pygame.font.SysFont("Calibri", 30,'bold')
    label = font.render("LUDO GAME", 1, 'black')

    while (True):
        for event in pygame.event.get():
            if(withComputer and currentPlayer=='R') or event.type == MOUSEBUTTONDOWN:
                if(withComputer and currentPlayer=='R'):
                    loc=compLoc(random.randint(1, 6))
                    dice_clicked == True
                elif event.type == MOUSEBUTTONDOWN:
                    loc = gridlocation(event.pos)
                if (loc[0] >= 16 and loc[0] <= 18 and loc[1] >= 6 and loc[1] <= 8 and dice_clicked == False):
                    # dice_value = 6
                    diceValue = random.randint(1, 6)
                    print("dice clicked", currentPlayer)
                    dice_clicked = True
                if diceValue != 6 and dice_clicked == True:
                    print(1)
                    flag = 0
                    for i in cList:
                        for p in Game_grid[i[0]][i[1]].playerList:
                            if p.Id[0] == currentPlayer:
                                flag = 1
                    if flag == 0:
                        nextPlayer()
                        dice_clicked = False

                if currentPlayer == 'R' and diceValue == 6 and (loc in [(1, 1), (4, 1), (4, 4), (1, 4)]) and dice_clicked == True:
                    print(2)
                    print(Game_grid[1][6].playerList)
                    Game_grid[1][6].playerList.append(Game_grid[loc[0]][loc[1]].playerList[0])
                    Game_grid[1][6].playerList[-1].coordinates = (50 * 1, 50 * 6)
                    for p in Game_grid[1][6].playerList:
                        print(p.coordinates)
                    Game_grid[loc[0]][loc[1]].playerList = []
                    dice_clicked = False
                elif currentPlayer == 'G' and diceValue == 6 and (loc in [(10, 1), (13, 1), (13, 4), (10, 4)]) and dice_clicked == True:
                    print(3)
                    print(Game_grid[8][1].playerList)
                    Game_grid[8][1].playerList.append(Game_grid[loc[0]][loc[1]].playerList[0])
                    Game_grid[8][1].playerList[-1].coordinates = (50 * 8, 50 * 1)
                    Game_grid[loc[0]][loc[1]].playerList = []
                    print(Game_grid[8][1].playerList[0].Id)
                    dice_clicked = False
                elif currentPlayer == 'B' and diceValue == 6 and (loc in [(1, 10), (4, 10), (4, 13), (1, 13)]) and dice_clicked == True:
                    print(5)
                    print(Game_grid[6][13].playerList)
                    Game_grid[6][13].playerList.append(Game_grid[loc[0]][loc[1]].playerList[0])
                    Game_grid[6][13].playerList[-1].coordinates = (50 * 6, 50 * 13)
                    Game_grid[loc[0]][loc[1]].playerList = []
                    dice_clicked = False

                elif currentPlayer == 'Y' and diceValue == 6 and (loc in [(10, 10), (13, 10), (13, 13), (10, 13)]) and dice_clicked == True:
                    print(4)
                    print(Game_grid[13][8].playerList)
                    Game_grid[13][8].playerList.append(Game_grid[loc[0]][loc[1]].playerList[0])
                    Game_grid[13][8].playerList[-1].coordinates = (50 * 13, 50 * 8)
                    Game_grid[loc[0]][loc[1]].playerList = []
                    dice_clicked = False


                elif currentPlayer == 'R' and (loc in [(1, 7), (2, 7), (3, 7), (4, 7), (5, 7)]) and len(
                        Game_grid[loc[0]][loc[1]].playerList) > 0 and dice_clicked == True:
                    if loc[0] + diceValue <= 6:
                        Game_grid[loc[0] + diceValue][loc[1]].playerList.append(Game_grid[loc[0]][loc[1]].playerList[-1])
                        Game_grid[loc[0] + diceValue][loc[1]].playerList[-1].coordinates = (
                        50 * (loc[0] + diceValue), 50 * (loc[1]))
                        Game_grid[loc[0]][loc[1]].playerList = Game_grid[loc[0]][loc[1]].playerList[:-1]
                    dice_clicked = False

                elif currentPlayer == 'G' and (loc in [(7, 1), (7, 2), (7, 3), (7, 4), (7, 5)]) and len(
                        Game_grid[loc[0]][loc[1]].playerList) > 0 and dice_clicked == True:
                    if loc[1] + diceValue <= 6:
                        Game_grid[loc[0]][loc[1] + diceValue].playerList.append(Game_grid[loc[0]][loc[1]].playerList[-1])
                        Game_grid[loc[0]][loc[1] + diceValue].playerList[-1].coordinates = (
                            50 * (loc[0]), 50 * (loc[1] + diceValue))
                        Game_grid[loc[0]][loc[1]].playerList = Game_grid[loc[0]][loc[1]].playerList[:-1]
                    dice_clicked = False

                elif currentPlayer == 'B' and (loc in [(7, 9), (7, 10), (7, 11), (7, 12), (7, 13)]) and len(
                        Game_grid[loc[0]][loc[1]].playerList) > 0 and dice_clicked == True:
                    if loc[1] + diceValue >= 8:
                        Game_grid[loc[0]][loc[1] + diceValue].playerList.append(Game_grid[loc[0]][loc[1]].playerList[-1])
                        Game_grid[loc[0]][loc[1] + diceValue].playerList[-1].coordinates = (
                            50 * (loc[0]), 50 * (loc[1] + diceValue))
                        Game_grid[loc[0]][loc[1]].playerList = Game_grid[loc[0]][loc[1]].playerList[:-1]
                    dice_clicked = False

                elif currentPlayer == 'Y' and (loc in [(9, 7), (10, 7), (11, 7), (12, 7), (13, 7)]) and len(
                    Game_grid[loc[0]][loc[1]].playerList) > 0 and dice_clicked == True:
                    if loc[0] - diceValue >=8:
                        Game_grid[loc[0] - diceValue][loc[1]].playerList.append(Game_grid[loc[0]][loc[1]].playerList[-1])
                        Game_grid[loc[0] - diceValue][loc[1]].playerList[-1].coordinates = (
                            50 * (loc[0] - diceValue), 50 * (loc[1]))
                        Game_grid[loc[0]][loc[1]].playerList = Game_grid[loc[0]][loc[1]].playerList[:-1]
                    dice_clicked = False

                elif (check(loc)) and checkId(Game_grid[loc[0]][loc[1]].playerList) and dice_clicked == True:
                    print(6)
                    newpos = move(loc, diceValue, currentPlayer)
                    new_list = []
                    flg = 0
                    for i in Game_grid[loc[0]][loc[1]].playerList:
                        if i.Id[0] == currentPlayer and flg == 0:
                            Game_grid[newpos[0]][newpos[1]].playerList.append(i)
                            Game_grid[newpos[0]][newpos[1]].playerList[-1].coordinates = (50 * newpos[0], 50 * newpos[1])
                            #eating pieces
                            Game_grid[newpos[0]][newpos[1]].playerList=checkCollision(Game_grid[newpos[0]][newpos[1]].playerList)
                            flg = 1
                        else:
                            new_list.append(i)
                    Game_grid[loc[0]][loc[1]].playerList = new_list
                    dice_clicked = False

                    if diceValue != 6:
                        nextPlayer()

                # DISPLAYSURF.blit(drawGrid(), (0, 0))
                # pygame.display.update()
            font1 = pygame.font.SysFont("Calibri", 50)
            label1 = font1.render(str(diceValue), 1, 'black')

            DISPLAYSURF.blit(drawGrid(), (0, 0))
            DISPLAYSURF.blit(label, (800, 10))
            DISPLAYSURF.blit(label1, (850, 500))
            pygame.display.update()


            if event.type == QUIT:
                pygame.quit()
                sys.exit()

pygame.init()
screen = pygame.display.set_mode((1000, 600))
pygame.display.set_caption('PythonGeeks Ludo Game')
clock = pygame.time.Clock()
font = pygame.font.SysFont("Arial", 20)

class Button:
    """Create a button, then blit the surface in the while loop"""

    def __init__(self, text,num,comp,pos, font, bg="blue", feedback=""):
        self.x, self.y = pos
        self.font = pygame.font.SysFont("Arial", font)
        self.no=num
        self.text=text
        self.text = self.font.render(self.text, 1, pygame.Color("White"))
        self.cmp=comp
        self.change_text(bg)

    def change_text(self, bg="blue"):
        self.size = self.text.get_size()
        self.surface = pygame.Surface(self.size)
        self.surface.fill(bg)
        self.surface.blit(self.text, (0, 0))
        self.rect = pygame.Rect(self.x, self.y, self.size[0], self.size[1])

    def show(self):
        screen.blit(self.text , (self.x, self.y))

    def click(self, event):
        x, y = pygame.mouse.get_pos()
        font1 = pygame.font.SysFont("Calibri", 50)
        label1 = font1.render("PythonGeeks Ludo Game", 1, 'yellow')
        screen.blit(label1, (230, 30))
        if event.type == pygame.MOUSEBUTTONDOWN:
            if pygame.mouse.get_pressed()[0]:
                if self.rect.collidepoint(x, y):
                    global n,withComputer
                    n=self.no
                    withComputer=self.cmp
                    print(n,",",withComputer)
                    pygame.quit()
                    mainGame()


def mainloop():
    """ The infinite loop where things happen """
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            button1.click(event)
            button2.click(event)
            button3.click(event)
            button4.click(event)
        button1.show()
        button2.show()
        button3.show()
        button4.show()

        clock.tick(30)
        pygame.display.update()


button1 = Button(
    "Play with Computer",2,True,
    (400, 150),
    font=30,
    bg="navy")


button2 = Button(
    "2 Players",2,False,
    (400, 250),
    font=30,
    bg="navy")

button3 = Button(
    "3 Players",3,False,
    (400, 350),
    font=30,
    bg="navy",)

button4 = Button(
    "4 Players",4,False,
    (400, 450),
    font=30,
    bg="navy",)

mainloop()

