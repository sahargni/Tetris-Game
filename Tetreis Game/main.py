from shapes import *
import pygame
import random
import sys

pygame.init()

myShapes = [T, L, LP, LINE, Z, ZP, O]

block_size = 25

win_Width = 800
win_Height = 650

window_size = (win_Width, win_Height)
pygame.display.set_caption("TetrisProject")
window = pygame.display.set_mode(window_size)


rows = 20
columns = 10


x_side = (win_Width - (block_size * columns)) / 2
y_side = 35

nextShape = random.randint(0, len(myShapes) - 1)
nextcolor = random.randint(1, len(colors) - 1)

def Barkhord():
    global sheklMan, Data, x, y
    intersect = False
    for i in range(len(sheklMan)):
        for j in range(len(sheklMan)):
            if sheklMan[i][j] > 0:
                if i + y > 19 or j + x > 9 or j + x < 0 or Data[i + y][j + x] > 0:
                    intersect = True
    print("intersect is: " , intersect)
    return intersect

def updateVars():
    global x, y, rotation, sh_type, random_color, sheklMan, nextShape, nextcolor
    x = 3
    y = 2
    rotation = 0
    # sh_type = random.randint(0, len(myShapes) - 1)
    sh_type = nextShape
    # sh_type = 3
    random_color = nextcolor
    sheklMan = myShapes[sh_type][rotation]
    nextShape = random.randint(0, len(myShapes) - 1)
    nextcolor = random.randint(1, len(colors) - 1)

def newGame():
    updateVars()
    global gameState, Data, Score, default_fps, default_speed
    gameState = "start"
    Score = 0
    default_fps = 35
    default_speed = 30
    Data = []
    for i in range(rows):
        temp = []
        for j in range(columns):
            temp.append(0)
        Data.append(temp)

def BreakLine():
    global Data, x, y, Score

    for i in range(4):
        for j in range(4):
            if sheklMan[i][j] > 0:
                Data[i + y][j + x] = random_color

    khatShomar = 0
    for i in range(rows):
        sefrShomar = 0
        for j in range(columns):
            if Data[i][j] > 0:
                sefrShomar += 1
        if sefrShomar > 9:
            for k in range(i, 1, -1):
                for h in range(columns):
                    Data[k][h] = Data[k - 1][h]
            khatShomar += 1
    Score += khatShomar ** 2

def RotateShape():
    global sheklMan, sh_type, rotation
    Rot_backup = rotation
    rotation = (rotation + 1) % len(myShapes[sh_type])
    sheklMan = myShapes[sh_type][rotation]
    if Barkhord():
        rotation = Rot_backup
    sheklMan = myShapes[sh_type][rotation]

def goSpace():
    global sheklMan, y
    while not Barkhord():
        y += 1
        sheklMan = myShapes[sh_type][rotation]
    y -= 1
    sheklMan = myShapes[sh_type][rotation]
    BreakLine()
    nextShape = random.randint(0, len(myShapes) - 1)
    updateVars()

newGame()


fps = default_fps
Speed = default_speed
Counter = 0

isGameRuning = True
while isGameRuning:
    back_Color = darkCyan
    window.fill(back_Color)
    if (gameState == "start") and (Counter % Speed == 0):
        Counter = 0
        y += 1
        if Barkhord():
            y -= 1
            BreakLine()

            for k in Data:
                print(k)
            updateVars()
            if Barkhord():
                gameState = "gameover"

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            isGameRuning = False
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                newGame()
            if gameState == "start":
                if event.key == pygame.K_RIGHT:
                    x += 1
                    if Barkhord():
                        x -= 1
                if event.key == pygame.K_LEFT:
                    x -= 1
                    if Barkhord():
                        x += 1
                if event.key == pygame.K_UP:
                    RotateShape()
                if event.key == pygame.K_DOWN:
                    fps = 120
                    Speed = 3
                if event.key == pygame.K_SPACE:
                    goSpace()
                    if Barkhord():
                        gameState = "gameover"
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_DOWN:
                fps = default_fps
                Speed = default_speed

    # جدول تتریس
    for i in range(rows):
        for j in range(columns):
            pygame.draw.rect(window, (255, 255, 255), ((x_side + j * block_size, y_side + i * block_size ), (block_size, block_size)), 1)
            if Data[i][j] > 0:
                pygame.draw.rect(window, colors[Data[i][j]], ((x_side + j * block_size + 1, y_side + i * block_size + 1), (block_size - 2, block_size - 2)), 0)


    # رسم شکل ها
    for i in range(4):
        for j in range(4):
            if sheklMan[i][j] > 0:
                pygame.draw.rect(window, colors[random_color], ((x_side + ((x + j) * block_size) + 1, y_side + (i + y) * block_size + 1), (block_size - 2,block_size - 2)), 0)
            # else:
            #     pygame.draw.rect(window, salmon, ((x_side + ((x + j) * block_size) + 1, y_side + (i + y) * block_size + 1), (block_size - 2,block_size - 2)), 0)

    # shekl badi
    for i in range(4):
        for j in range(4):
            pygame.draw.rect(window, (255, 255, 255), ((win_Width - 150 + ((j) * block_size), 110 + (i) * block_size), (block_size ,block_size )), 1)
            if myShapes[nextShape][0][i][j] > 0:
                pygame.draw.rect(window, colors[nextcolor], ((win_Width - 150 + ((j) * block_size) + 1, 110 + (i) * block_size + 1), (block_size - 2,block_size - 2)), 0)

    font_1 = pygame.font.SysFont("calibri", 25, True)
    fon2_size = 75
    font_2 = pygame.font.SysFont("calibri", fon2_size, True)
    textColor = lightBlue
    ScoreText = font_1.render("Score: " + str(Score), True, textColor)

    alert_1 = font_2.render("Game Over !", True, blue)
    alert_2 = font_2.render("Press ESC", True, blue)
    alert_3 = font_1.render("Next Shape:", True, salmon)

    al3_x = (win_Width - (10 * 15))
    window.blit(alert_3, [al3_x, 80])

    window.blit(ScoreText, [0, 30])
    al1_x = (win_Width - (len("Game Over !") * (fon2_size - 35))) / 2
    al2_x = (win_Width - (len("Press ESC") * (fon2_size - 35))) / 2

    if gameState == "gameover":
        window.blit(alert_1, [al1_x, 400])
        window.blit(alert_2, [al2_x, 450])


    pygame.time.Clock().tick(fps)
    pygame.display.update()
    Counter += 1

# mahdic200