# http://2048game.com/


from PIL import ImageGrab, ImageOps
import pyautogui, time

currentGrid = [0, 0, 0, 0,
               0, 0, 0, 0,
               0, 0, 0, 0,
               0, 0, 0, 0]

UP = 100
LEFT = 101
DOWN = 102
RIGHT = 103

ScoreGrid = [50, 40, 30, 20,
             30, 8, 5,  7,
             10, 5,  4,  2,
             5, 2,  2,  0]

class Cords:

    cord11 = (280, 620)
    cord12 = (520, 620)
    cord13 = (760, 620)
    cord14 = (1000, 620)
    cord21 = (280, 860)
    cord22 = (520, 860)
    cord23 = (760, 860)
    cord24 = (1000, 860)
    cord31 = (280, 1100)
    cord32 = (520, 1100)
    cord33 = (760, 1100)
    cord34 = (1000, 1100)
    cord41 = (280, 1340)
    cord42 = (520, 1340)
    cord43 = (760, 1340)
    cord44 = (1000, 1340)

    cordArray = [cord11, cord12, cord13, cord14,
                 cord21, cord22, cord23, cord24,
                 cord31, cord32, cord33, cord34,
                 cord41, cord42, cord43, cord44]


# 2048 => 182  **
# 1024 => 187
# 512  => 190
# 256  => 195
# 128  => 199
# 64   => 127
# 32   => 148
# 16   => 164
# 8    => 182
# 4    => 220
# 2    => 226
# 0    => 186

class Values:
    empty = 194
    two = 229
    four = 224
    eight = 190
    sixteen = 171
    thirtyTwo = 157
    sixtyFour = 135
    oneTwentyEight = 205
    twoFiftySix = 201
    fiveOneTwo = 197
    oneZeroTwoFour = 193
    twoZeroFourEight = 189

    valueArray = [empty, two, four, eight, sixteen, thirtyTwo, sixtyFour, oneTwentyEight,
                  twoFiftySix, fiveOneTwo, oneZeroTwoFour, twoZeroFourEight]




def getGrid():
    image = ImageGrab.grab()
    grayImage = ImageOps.grayscale(image)

    for index, cord in enumerate(Cords.cordArray):
        pixel = grayImage.getpixel(cord)
        try:
            pos = Values.valueArray.index(pixel)
            if pos == 0:
                currentGrid[index] = 0
            else:
                currentGrid[index] = pow(2, pos)
        except:
            print("Warning! Check the color codes and the game position!")

def printGrid(grid):
    for i in range(16):
        if i%4 == 0:
            print("[ " + str(grid[i]) + " " + str(grid[i+1]) + " " + str(grid[i+2]) + " " + str(grid[i+3]) + " ]")


def swipeRow(row):
    prev = -1
    i = 0
    temp = [0, 0, 0, 0]

    for element in row:

        if element != 0:
            if prev == element:
                temp[i - 1] = 2 * prev
                prev = -1
            else:
                prev = element
                temp[i] = element
                i += 1

    return temp


def getNextGrid(grid, move):

    temp = [0, 0, 0, 0,
            0, 0, 0, 0,
            0, 0, 0, 0,
            0, 0, 0, 0]

    if move == UP:
        for i in range(4):
            row = []
            for j in range(4):
                row.append(grid[i + 4*j])
            row = swipeRow(row)
            for j, val in enumerate(row):
                temp[i + 4*j] = val

    elif move == LEFT:
        for i in range(4):
            row = []
            for j in range(4):
                row.append(grid[4*i + j])
            row = swipeRow(row)
            for j, val in enumerate(row):
                temp[4*i + j] = val

    elif move == DOWN:
        for i in range(4):
            row = []
            for j in range(4):
                row.append(grid[i + 4 * (3-j)])
            row = swipeRow(row)
            for j, val in enumerate(row):
                temp[i + 4 * (3-j)] = val

    elif move == RIGHT:
        for i in range(4):
            row = []
            for j in range(4):
                row.append(grid[4 * i + (3-j)])
            row = swipeRow(row)
            for j, val in enumerate(row):
                temp[4 * i + (3-j)] = val

    return temp


def getScore(grid):
    score=0
    for i in range(4):
        for j in range(4):
            score+=grid[4*i+j]*ScoreGrid[4*i+j]
    return score


def getBestMove(grid):
    scoreUp=getScore(getNextGrid(grid,UP))
    scoreDown = getScore(getNextGrid(grid, DOWN))
    scoreLeft = getScore(getNextGrid(grid, LEFT))
    scoreRight = getScore(getNextGrid(grid, RIGHT))

    if not isMoveValid(grid,UP):
        scoreUp=0
    if not isMoveValid(grid,DOWN):
        scoreDown=0
    if not isMoveValid(grid,LEFT):
        scoreLeft=0
    if not isMoveValid(grid,RIGHT):
        scoreRight=0

    maxScore=max(scoreUp,scoreDown,scoreLeft,scoreRight)

    if scoreUp == maxScore:
        return UP
    elif scoreDown == maxScore:
        return DOWN
    elif scoreLeft == maxScore:
        return LEFT
    else:
        return RIGHT


def isMoveValid(grid,move):
    if getNextGrid(grid,move) == grid:
        return False
    else:
        return True

def performMove(move):
    if move == UP:
        pyautogui.keyDown('up')
        pyautogui.keyUp('up')
    elif move == DOWN:
        pyautogui.keyDown('down')
        pyautogui.keyUp('down')
    elif move == LEFT:
        pyautogui.keyDown('left')
        pyautogui.keyUp('left')
    else:
        pyautogui.keyDown('right')
        pyautogui.keyUp('right')

def main():
    time.sleep(3)
    while True:
        getGrid()
        performMove(getBestMove(currentGrid))
        time.sleep(0.03)

if __name__  ==  '__main__':
    main()
