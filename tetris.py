import pygame
import random


pygame.font.init()

# Konstandid
ekraaniLaius = 800
ekraaniPikkus = 700
mänguLaius = 300
mänguPikkus = 600
plokiSuurus = 30

topLeftX = (ekraaniLaius - mänguLaius) // 2
topLeftY = ekraaniPikkus - mänguPikkus

# Kujundid ja nende võimalikud asendid

S = [['.....',
      '......',
      '..00..',
      '.00...',
      '.....'],
     ['.....',
      '..0..',
      '..00.',
      '...0.',
      '.....']]

Z = [['.....',
      '.....',
      '.00..',
      '..00.',
      '.....'],
     ['.....',
      '..0..',
      '.00..',
      '.0...',
      '.....']]

I = [['..0..',
      '..0..',
      '..0..',
      '..0..',
      '.....'],
     ['.....',
      '0000.',
      '.....',
      '.....',
      '.....']]

O = [['.....',
      '.....',
      '.00..',
      '.00..',
      '.....']]

J = [['.....',
      '.0...',
      '.000.',
      '.....',
      '.....'],
     ['.....',
      '..00.',
      '..0..',
      '..0..',
      '.....'],
     ['.....',
      '.....',
      '.000.',
      '...0.',
      '.....'],
     ['.....',
      '..0..',
      '..0..',
      '.00..',
      '.....']]

L = [['.....',
      '...0.',
      '.000.',
      '.....',
      '.....'],
     ['.....',
      '..0..',
      '..0..',
      '..00.',
      '.....'],
     ['.....',
      '.....',
      '.000.',
      '.0...',
      '.....'],
     ['.....',
      '.00..',
      '..0..',
      '..0..',
      '.....']]

T = [['.....',
      '..0..',
      '.000.',
      '.....',
      '.....'],
     ['.....',
      '..0..',
      '..00.',
      '..0..',
      '.....'],
     ['.....',
      '.....',
      '.000.',
      '..0..',
      '.....'],
     ['.....',
      '..0..',
      '.00..',
      '..0..',
      '.....']]
yellow = (255,255,204)
shapes = [S, Z, I, O, J, L, T]
shapeColors = [(0, 255, 0), (255, 0, 0), (0, 255, 255), (255, 255, 0), (255, 165, 0), (0, 0, 255), (128, 0, 128)]
# index 0 - 6 kujundi vastavus
objektid = []

#Teeb tüki objektiks  Vaja oli interneeduse abi et kujund valmistada
class Piece(object):
    def __init__(self, x, y, shape):
        self.x = x
        self.y = y
        self.shape = shape
        self.color = shapeColors[shapes.index(shape)]
        self.rotation = 0

# teeb mängulaua, kus on ka olema hõivatud väljad, kui neid esineb     Ise tehtud
def createGrid(lockedPositions={}):
    grid = [[(0, 0, 0) for _ in range(10)] for _ in range(20)]

    for i in range(len(grid)):
        for j in range(len(grid[i])):
            if (j, i) in lockedPositions:
                c = lockedPositions[(j, i)]
                grid[i][j] = c

    return grid

# Konverteerib kujundi    Oli abi vaja
def convertShapeFormat(shape):
    positions = []
    formatShape = shape.shape[shape.rotation % len(shape.shape)]

    for i, line in enumerate(formatShape):
        row = list(line)
        for j, column in enumerate(row):
            if column == '0':
                positions.append((shape.x + j, shape.y + i))

    for i, pos in enumerate(positions):
        positions[i] = (pos[0] - 2, pos[1] - 4)

    return positions

#Kontrollib, kas järgmine ruut on vaba  acceptedPosiga oli natukene jamasti
def validSpace(shape, grid):
    acceptedPos = [[(j, i) for j in range(10) if grid[i][j] == (0, 0, 0)] for i in range(20)]
    acceptedPos = [j for sub in acceptedPos for j in sub]

    formatted = convertShapeFormat(shape)

    for pos in formatted:
        if pos not in acceptedPos:
            if pos[1] > -1:
                return False
    return True

#Kontrollib, kas on kaotus   Sain ise hakkama
def checkLost(positions):
    for pos in positions:
        x, y = pos
        if y < 1:
            return True

    return False

# Kujundi valik    Kujundi loomisel oli abi vaja
def getShape():
    global objektid
    if len(objektid) == 0:
        teeObjektid()
    piece = random.choice(objektid)
    objektid.remove(piece)
    return Piece(5, 0, piece)

#Kujundi loomine
def teeObjektid():
    global objektid
    objektid = shapes.copy()

# Kiri keskele  Videod!!!
def drawTextMiddle(text, size, color, surface):
    font = pygame.font.SysFont('freesansbol.tff', size, bold=True)
    label = font.render(text, 1, color)
    surface.blit(label, (topLeftX + mänguLaius/2 - (label.get_width()/2), topLeftY + mänguPikkus/2 - (label.get_height()/2)))

# Ruudustik Leboo!!
def drawGrid(surface, grid):
    sx = topLeftX
    sy = topLeftY

    for i in range(len(grid)):
        pygame.draw.line(surface, (128, 128, 128), (sx, sy + i * plokiSuurus), (sx + mänguLaius, sy + i * plokiSuurus))
        for j in range(len(grid[1])):
            pygame.draw.line(surface, (128, 128, 128), (sx + j * plokiSuurus, sy),
                             (sx + j * plokiSuurus, sy + mänguPikkus))

#Kui rida on täis, siis tühjendab selle
def clearRows(grid, locked):
    inc = 0

    for i in range(len(grid)-1, -1, -1):
        row = grid[i]
        if (0, 0, 0) not in row:
            inc += 1
            ind = i

            for j in range(len(row)):
                try:
                    del locked[(j, i)]
                except:
                    continue

    if inc > 0:
        for key in sorted(list(locked), key=lambda x: x[1])[::-1]:
            x, y = key
            if y < ind:
                newkey = (x, y + inc)
                locked[newkey] = locked.pop(key)

    return inc

#Järgmine tükk, mis tuleb
def drawNextShape(shape, surface):
    font = pygame.font.SysFont('freesansbol.tff', 30)
    label = font.render('Järgmine tükk', 1, (255, 255, 255))

    sx = topLeftX + mänguLaius + 50
    sy = topLeftY + mänguPikkus/2 - 100
    formatShape = shape.shape[shape.rotation % len(shape.shape)]

    for i, line in enumerate(formatShape):
        row = list(line)
        for j, column in enumerate(row):
            if column == '0':
                pygame.draw.rect(surface, shape.color, (sx + j*plokiSuurus, sy + i*plokiSuurus, plokiSuurus, plokiSuurus), 0)

    surface.blit(label, (sx + 10, sy - 30))  # TODO add borders to the pieces

#Joonistab käes oleva kujundi
def drawHeldShape(shape, surface):
    font = pygame.font.SysFont('freesansbol.tff', 30)
    label = font.render('Käes olev tükk', 1, (255, 255, 255))

    sx = topLeftX - mänguLaius + 50
    sy = topLeftY + mänguPikkus/2 - 100

    if shape is not None:
        formatShape = shape.shape[shape.rotation % len(shape.shape)]

        for i, line in enumerate(formatShape): #Enumeratega oli abi vaja
            row = list(line)
            for j, column in enumerate(row):
                if column == '0':
                    pygame.draw.rect(surface, shape.color, (sx + j*plokiSuurus, sy + i*plokiSuurus, plokiSuurus, plokiSuurus), 0)

    surface.blit(label, (sx + 10, sy - 30))

#Algne ekraan    Pff Leboo!!
def drawWindow(surface, grid, score=0):
    surface.fill((0, 0, 0))

    font = pygame.font.SysFont('freesansbold.ttf', 60)
    label = font.render('Tetris', 1, (255, 255, 255))

    surface.blit(label, (topLeftX + mänguLaius / 2 - (label.get_width() / 2), 30))

    for i in range(len(grid)):
        for j in range(len(grid[i])):
            pygame.draw.rect(surface, grid[i][j], (topLeftX + j*plokiSuurus, topLeftY +i*plokiSuurus, plokiSuurus, plokiSuurus), 0)
    pygame.draw.rect(surface, (255, 0, 0), (topLeftX, topLeftY, mänguLaius, mänguPikkus), 5)

    font = pygame.font.SysFont('freesansbol.tff', 30)
    label = font.render('Skoor: ' + str(score), 1, (255, 255, 255))

    sx = topLeftX + mänguLaius + 50
    sy = topLeftY + mänguPikkus / 2 - 100

    surface.blit(label, (sx + 20, sy + 160))
    drawGrid(surface, grid)

def pause():
    while True:
       win.fill((0, 0, 0))
       drawTextMiddle("Mäng pausil!!! Jätkamiseks vajuta ESC", 50, yellow, win)
       pygame.display.update()
       for event in pygame.event.get():
           if event.type == pygame.QUIT:
               return False
           if event.type == pygame.KEYDOWN:
               if event.key == pygame.K_ESCAPE:
                return True


# Vahetab tüki, kui on space alla vajutatud   Arusaadav täiesti
def holdPiece(currentPiece, heldPiece, nextPiece):
    if heldPiece is None:
        heldPiece = currentPiece
        currentPiece = nextPiece
        nextPiece = getShape()
    else:
        heldPiece, currentPiece = currentPiece, heldPiece
    return currentPiece, heldPiece, nextPiece

# Mängu jooksutamine
def main():
    lockedPositions = {}

    changePiece = False
    run = True
    currentPiece = getShape()
    nextPiece = getShape()
    heldPiece = None
    holdUsed = False
    clock = pygame.time.Clock()
    fallTime = 0
    score = 0

    #while tsükkel oli ise tehtud
    while run:
        grid = createGrid(lockedPositions)
        fallSpeed = max((0.27 - int(score/50)*0.01), 0.10)
        fallTime += clock.get_rawtime()
        clock.tick()

        if fallTime/1000 > fallSpeed:
            fallTime = 0
            currentPiece.y += 1
            if not validSpace(currentPiece, grid) and currentPiece.y > 0:
                currentPiece.y -= 1
                changePiece = True

        #Klahvid ja asjad   (kõik ise)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            if event.type == pygame.KEYDOWN:
                if event.key in (pygame.K_LEFT, pygame.K_a):
                    currentPiece.x -= 1
                    if not validSpace(currentPiece, grid):
                        currentPiece.x += 1

                if event.key in (pygame.K_RIGHT, pygame.K_d):
                    currentPiece.x += 1
                    if not validSpace(currentPiece, grid):
                        currentPiece.x -= 1

                if event.key in (pygame.K_DOWN, pygame.K_s):
                    currentPiece.y += 1
                    if not validSpace(currentPiece, grid):
                        currentPiece.y -= 1

                if event.key in (pygame.K_UP, pygame.K_w):
                    currentPiece.rotation += 1
                    if not validSpace(currentPiece, grid):
                        currentPiece.rotation -= 1

                if event.key in (pygame.K_SPACE, pygame.K_h):
                    if not holdUsed:
                        currentPiece, heldPiece, nextPiece = holdPiece(currentPiece, heldPiece, nextPiece)
                        currentPiece.x, currentPiece.y = 5, 0
                        holdUsed = True

                if event.key == pygame.K_c:
                    while True:
                        currentPiece.y += 1
                        if not validSpace(currentPiece, grid):
                            currentPiece.y -= 1
                            break

                if event.key == pygame.K_ESCAPE:
                     run = pause()


        shapePos = convertShapeFormat(currentPiece)

        for i in range(len(shapePos)):
            x, y = shapePos[i]
            if y > -1:
                grid[y][x] = currentPiece.color

        if changePiece:
            for pos in shapePos:
                p = (pos[0], pos[1])
                lockedPositions[p] = currentPiece.color

            currentPiece = nextPiece
            nextPiece = getShape()
            changePiece = False
            holdUsed = False

            score += clearRows(grid, lockedPositions) * 10
        #Joonistamine
        drawWindow(win, grid, score)
        drawNextShape(nextPiece, win)
        drawHeldShape(heldPiece, win)
        pygame.display.update()
        #Kaotus kontroll, kui õige, if == True, siis lõpetab mängu
        if checkLost(lockedPositions):
            drawTextMiddle('Nelson: "Haw! Haw!', 80, (255, 255, 255), win)
            pygame.display.update()
            pygame.time.delay(1500)
            run = False

#Esimene kaader mängus
def mainMenu():
    run = True
    while run:
        win.fill((0, 0, 0))
        drawTextMiddle("Alustamiseks vajuta ükskõik mida", 50, yellow, win)
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.KEYDOWN:
                main()
    pygame.display.quit()


win = pygame.display.set_mode((ekraaniLaius,ekraaniPikkus))
pygame.display.set_caption('Tetris')
mainMenu()  # mäng algab
