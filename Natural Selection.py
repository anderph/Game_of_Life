import math
import numpy as np
import PySimpleGUI as sg
import matrixManipulation as mm
import random
import time

# variable setup

initialChanceOfLife = .3
chanceOfDeath = 0.015
chanceOfBirth = 0.005
matricesPerGeneration = 15
generationLength = 70
outerBoundaryCheck = 100  # how far away from the origin the win conditions will be checked
randomStartBoundary = 30  # this amount in all directions from origin
winConditionBoundary = randomStartBoundary + 10
originx = round(mm.matrix_size / 2)
originy = round(mm.matrix_size / 2)
winningGeneration = np.zeros((mm.matrix_size, mm.matrix_size))  # blank matrix
listOfGensToCompete = np.zeros((matricesPerGeneration, mm.matrix_size, mm.matrix_size))
listOfGensToPlay = np.zeros((matricesPerGeneration, mm.matrix_size, mm.matrix_size))
displayedGeneration = winningGeneration
evolutionCount = 0
evoCounter = 0  # this is for repeatedly evolving from the terminal

displayedMatrixCountCalculated = 0

# default variable definition for displaying
size_of_grid = 768  # resolution in width/length of pixels
cell_width = 10
cells_to_fit = math.floor(size_of_grid / cell_width / 2) * 2
grid_lines = True
run_once = True

matrix_x_position = originx
matrix_y_position = originy


# random start matrix is created
def randomInitialMatrixCreation():
    for x in range(-randomStartBoundary, randomStartBoundary):
        for y in range(-randomStartBoundary, randomStartBoundary):
            if random.random() < initialChanceOfLife:
                winningGeneration[originx + x, originy + y] = 1
                # print(x)


# this is the iteration algorithm that takes the best one and modifies it 9 times (10 if unmodified is included)

def iterateMatrix():
    global listOfGensToCompete
    listOfGensToCompete = np.zeros((matricesPerGeneration, mm.matrix_size, mm.matrix_size))
    listOfGensToCompete[0] = winningGeneration
    for numberOfMatrices in range(matricesPerGeneration - 1):
        tempMatrix = winningGeneration
        for x in range(-randomStartBoundary, randomStartBoundary):
            for y in range(-randomStartBoundary, randomStartBoundary):
                if tempMatrix[originx + x, originy + y] == 1:
                    if random.random() < chanceOfDeath:
                        # print("change to 0")
                        tempMatrix[originx + x, originy + y] = 0
                        # print(tempMatrix[originx + x, originy + y])
                if tempMatrix[originx + x, originy + y] == 0:
                    if random.random() < chanceOfBirth:
                        tempMatrix[originx + x, originy + y] = 1
        # tempMatrix[168:178, 170] = [1,1,1,1,1,1,1,1,1,1]
        # tempMatrix[168:178, 171] = [1,1,1,1,1,1,1,1,1,1]
        # print(tempMatrix[(originx - randomStartBoundary):(originx + randomStartBoundary), (originy - randomStartBoundary):(originy + randomStartBoundary)])
        listOfGensToCompete[numberOfMatrices + 1] = tempMatrix
        # print(str(len(listOfGensToCompete)) + "length of list of gens to compete")
        # if listOfGensToCompete[0].all() == listOfGensToCompete[numberOfMatrices].all():
        #     print("fuck")
    # print(listOfGensToCompete)


def gameOfLifeTheMatrix():
    for genNumber in range(len(listOfGensToCompete)):
        tempMatrix = listOfGensToCompete[genNumber]
        for i in range(generationLength):
            tempMatrix = mm.next_generation(tempMatrix)
        listOfGensToPlay[genNumber] = (tempMatrix)


def winCondition1(matrix):
    tempgen1 = matrix[(originx - outerBoundaryCheck):(originx + outerBoundaryCheck),
               (originy - outerBoundaryCheck):(originy + outerBoundaryCheck)]
    total = np.count_nonzero(tempgen1)
    tempgen2 = matrix[(originx - winConditionBoundary):(originx + winConditionBoundary),
               (originy - winConditionBoundary):(originy + winConditionBoundary)]
    innerWinBoundary = np.count_nonzero(tempgen2)
    outsideWinBoundary = total - innerWinBoundary
    # print(total)
    # print(innerWinBoundary)
    # print(outsideWinBoundary)
    return outsideWinBoundary


def winCondition2(matrix):
    print()


def winCondition3(matrix):
    print()


def winCondition4(matrix):
    print()


def cullTheMatrix():
    winStates = []
    for gen in listOfGensToPlay:
        winStates.append(winCondition1(gen))
        # winCondition2(gen)
        # winCondition3(gen)
        # winCondition4(gen)
    print("winStates are :" + str(winStates))
    return winStates.index(max(winStates))


def update_text():
    window['output'].update(str("current matrix # = " + str((displayedMatrixCountCalculated % matricesPerGeneration)) +
                                ' winCondition = ' + str(
        winCondition1(listOfGensToPlay[displayedMatrixCountCalculated % matricesPerGeneration])) +
                                " and top performer = " + str(cullTheMatrix()) + ", current evolution = " + str(
        evolutionCount)))
    window['top out'].update("EvoCounterStack = " + str(evoCounter))


def initialStart():  ## technically, this chooses the best matrix from 15 totally random ones, so the IA isn't entirely
    # accurate, but it might as well be and I think this is a better method regardless
    global winningGeneration  ## Important this is where the initial matrix function is called
    for i in range(matricesPerGeneration):
        randomInitialMatrixCreation()
        listOfGensToCompete[i] = winningGeneration
        winningGeneration = np.zeros((mm.matrix_size, mm.matrix_size))
    gameOfLifeTheMatrix()
    print(cullTheMatrix())
    winningGeneration = listOfGensToCompete[cullTheMatrix()]


initialStart()


def evolution():
    global evolutionCount
    global winningGeneration
    evolutionCount += 1
    iterateMatrix()
    gameOfLifeTheMatrix()
    winningGeneration = listOfGensToCompete[cullTheMatrix()]
    update_text()


# GUI initialization

sg.theme('LightGreen2')  # background color

layout = [[sg.Graph((size_of_grid, size_of_grid), (0, 0), (size_of_grid, size_of_grid), key='GRAPH',
                    change_submits=True, drag_submits=False)],
          [sg.Text('Enter command:'), sg.InputText(key='terminal'), sg.Text((" " * 100), key='top out')],
          [sg.Button('Okay'), sg.Cancel(), sg.Text((" " * 170), key='output')]]

window = sg.Window('My new window', return_keyboard_events=True, use_default_focus=False).Layout(layout)
graph = window.Element('GRAPH')

event, values = window.Read()


# Function Definitions:

def visible_matrix():
    global visibleMatrix
    x = matrix_x_position
    y = matrix_y_position
    offset = round(cells_to_fit / 2)
    visibleMatrix = displayedGeneration[x - offset:x + offset, y - offset:y + offset]
    # print(visibleMatrix)


def draw_matrix():
    visible_matrix()
    live_cells = np.where(visibleMatrix == 1)
    # print(live_cells) #                    ccccccccccccccccccccccccccccccccccccccccccccccccc
    for i in range(len(live_cells[0])):
        x = live_cells[0][i]
        y = live_cells[1][i]

        top_left = ((x * cell_width), size_of_grid - (y * cell_width))
        bot_right = ((x * cell_width + cell_width), size_of_grid - (y * cell_width + cell_width))
        graph.DrawRectangle(top_left, bot_right, fill_color='red', line_color='red')


def draw_grid():
    if grid_lines:
        effective_grid_size = cells_to_fit * cell_width
        for i in range(cells_to_fit):
            graph.draw_line((i * cell_width, size_of_grid), (i * cell_width, size_of_grid - effective_grid_size))
        for i in range(cells_to_fit):
            graph.draw_line((0, size_of_grid - i * cell_width), (effective_grid_size, size_of_grid - i * cell_width))


def update_graph():
    graph.erase()
    draw_matrix()
    draw_grid()


def print_GUI_info():
    print('cell width: ' + str(cell_width))
    print('cells_to_fit: ' + str(cells_to_fit))
    print('grid_lines_status: ' + str(grid_lines))
    print('matrix_x_position: ' + str(matrix_x_position))
    print('matrix_y_position: ' + str(matrix_y_position))


def navigate(direction):
    global matrix_y_position
    global matrix_x_position
    if direction == 'Up':
        matrix_y_position -= round(96 / cell_width)
    elif direction == 'Down':
        matrix_y_position += round(96 / cell_width)
    elif direction == 'Right':
        matrix_x_position += round(96 / cell_width)
    elif direction == 'Left':
        matrix_x_position -= round(96 / cell_width)
        update_graph()


def keypress_check():
    global cell_width
    global cells_to_fit
    if 'Up' in event:
        navigate('Up')
    if 'Down' in event:
        navigate('Down')
    if 'Left' in event:
        navigate('Left')
    if 'Right' in event:
        navigate('Right')
    if ',' in event:
        cell_width -= 1
        cells_to_fit = math.floor(size_of_grid / cell_width / 2) * 2
    if '.' in event:
        cell_width += 1
        cells_to_fit = math.floor(size_of_grid / cell_width / 2) * 2


def process_terminal():
    # print(mm.gen_saver)
    global grid_lines
    global cell_width
    global cells_to_fit
    global displayedGeneration
    global displayedMatrixCountCalculated
    global evoCounter
    if values['terminal'] == 'size up':
        cell_width += 1
        cells_to_fit = math.floor(size_of_grid / cell_width / 2) * 2
    elif values['terminal'] == 'grid':
        grid_lines = not grid_lines
    elif values['terminal'] == 'firstCalculated':
        displayedMatrixCountCalculated = 0
        displayedGeneration = listOfGensToCompete[0]
    elif values['terminal'] == 'nextCalculated':
        displayedMatrixCountCalculated += 1
        displayedGeneration = listOfGensToCompete[(displayedMatrixCountCalculated % matricesPerGeneration)]
        update_text()
        # print(listOfGensToCompete)
        # print(winningGeneration)
        # print(len(listOfGensToCompete))
        # print(displayedGeneration[200,200])
        # print(listOfGensToCompete[(displayedMatrixCountCalculated % matricesPerGeneration)][200,200])
        # print(displayedMatrixCountCalculated % matricesPerGeneration)
        # print(listOfGensToCompete[(displayedMatrixCountCalculated % matricesPerGeneration)][170:230,170:230])
        update_graph()
    elif values['terminal'] == 'nextPlayed':
        displayedMatrixCountCalculated += 1
        displayedGeneration = listOfGensToPlay[(displayedMatrixCountCalculated % matricesPerGeneration)]
        update_text()
    elif values['terminal'] == 'original':
        displayedGeneration = listOfGensToCompete[(displayedMatrixCountCalculated % matricesPerGeneration)]
    elif values['terminal'] == 'win1':
        winCondition1(listOfGensToPlay[displayedMatrixCountCalculated % matricesPerGeneration])
    elif values['terminal'] == 'play':
        displayedGeneration = listOfGensToPlay[(displayedMatrixCountCalculated % matricesPerGeneration)]
    elif values['terminal'] == 'evolve':
        evolution()
    elif values['terminal'] == 'game':
        displayedGeneration = mm.next_generation(displayedGeneration)
    elif values['terminal'] == 'evoCount':
        evoCounter += 1
        update_text()
    elif values['terminal'] == 'evoBig':
        for i in range(evoCounter):
            timeSinceGeneration = time.time()
            evolution()
            print("evolved from evoBig on evo: " + str(evolutionCount) + ", evo took " +
                  str((time.time() - timeSinceGeneration)) + " seconds")
        evoCounter = 0
    elif values['terminal'] == 'diag':
        print_GUI_info()
    else:
        navigate(values['terminal'])
    print('processed')


print_GUI_info()
update_text()

while True:  # Event Loop
    event, values = window.Read()
    if event is None:
        break
    if event in (sg.WIN_CLOSED, 'Exit'):
        break

    mouse = values['GRAPH']
    if event == 'GRAPH':
        if mouse == (None, None):
            continue
    if event == 'Okay':
        process_terminal()
    keypress_check()
    update_graph()
