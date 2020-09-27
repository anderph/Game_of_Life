# This is the Graphical Interface file.
#
# Here, I will allow the user to see the grid, change the grid size, go forward and back generations
import numpy as np
import PySimpleGUI as sg
import matrixManipulation as mm
import math

visibleMatrix = np.zeros((2, 2))  # 2,2 is arbitrary, used to assign it as a matrix type

# default variable definition
size_of_grid = 768
cell_width = 25
cells_to_fit = math.floor(size_of_grid / cell_width / 2) * 2
grid_line_width = 1

matrix_x_position = 15
matrix_y_position = 15


# Function Definitions:

def visible_matrix():
    global visibleMatrix
    x = matrix_x_position
    y = matrix_y_position
    offset = round(cells_to_fit / 2)
    visibleMatrix = mm.current_generation[x - offset:x + offset, y - offset:y + offset]
    print(visibleMatrix)


def locate_button_press():
    offset = round(cells_to_fit / 2)
    effective_grid_size = cells_to_fit * cell_width
    pos_x = mouse[0]
    pos_y = size_of_grid - mouse[1]  # inverted so that 0,0 is on top left (like matrix) instead of bottom left (graph)
    matrix_x = round((pos_x - cells_to_fit / 2) / effective_grid_size * cells_to_fit)  # rounds to nearest cell number
    matrix_y = round((pos_y - cells_to_fit / 2) / effective_grid_size * cells_to_fit)  # rounds to nearest cell number
    mm.current_generation[matrix_x - offset + matrix_x_position, matrix_y - offset + matrix_y_position] = \
            (not mm.current_generation[matrix_x, matrix_y]) * 1
                                                # flips the nearest
    print(matrix_y)

def draw_matrix():
    visible_matrix()
    live_cells = np.where(visibleMatrix == 1)
    print(live_cells)
    for i in range(len(live_cells[0])):
        x = live_cells[0][i]
        y = live_cells[1][i]

        top_left = ((x * cell_width), size_of_grid - (y * cell_width))
        bot_right = ((x * cell_width + cell_width), size_of_grid - (y * cell_width + cell_width))
        graph.DrawRectangle(top_left, bot_right, fill_color='red', line_color='red')


def draw_grid():
    for i in range(cells_to_fit):
        x = i
        for p in range(cells_to_fit):
            y = p

            top_left = ((x * cell_width), size_of_grid - (y * cell_width))
            bot_right = ((x * cell_width + cell_width), size_of_grid - (y * cell_width + cell_width))
            graph.DrawRectangle(top_left, bot_right, line_color='black')


def print_GUI_info():
    print('cell width: ' + str(cell_width))
    print('cells_to_fit: ' + str(cells_to_fit))
    print('grid_line_width: ' + str(grid_line_width))


print_GUI_info()

sg.theme('DarkAmber')  # background color

layout = [[sg.Graph((size_of_grid, size_of_grid), (0, 0), (size_of_grid, size_of_grid), key='GRAPH',
                    change_submits=True, drag_submits=False)],
          [sg.Text('Enter command:'), sg.InputText()],
          [sg.OK(), sg.Cancel()]]

window = sg.Window('My new window').Layout(layout)
graph = window.Element('GRAPH')

event, values = window.Read()

while True:  # Event Loop
    event, values = window.Read()
    if event is None:
        break
    if event in (sg.WIN_CLOSED, 'Exit'):
        break

    graph.erase()
    draw_matrix()
    draw_grid()
    mm.next_generation()

    mouse = values['GRAPH']

    if event == 'GRAPH':
        if mouse == (None, None):
            continue
        locate_button_press()
        graph.erase()
        draw_matrix()
        draw_grid()
