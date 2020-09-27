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
cell_width = 10
cells_to_fit = math.floor(size_of_grid / cell_width / 2) * 2
grid_lines = True

matrix_x_position = 500
matrix_y_position = 500


# GUI initialization

sg.theme('DarkAmber')  # background color

layout = [[sg.Graph((size_of_grid, size_of_grid), (0, 0), (size_of_grid, size_of_grid), key='GRAPH',
                    change_submits=True, drag_submits=False)],
          [sg.Text('Enter command:'), sg.InputText(key='terminal')],
          [sg.Button('Okay'), sg.Cancel()]]

window = sg.Window('My new window').Layout(layout)
graph = window.Element('GRAPH')

event, values = window.Read()


# Function Definitions:

def visible_matrix():
    global visibleMatrix
    x = matrix_x_position
    y = matrix_y_position
    offset = round(cells_to_fit / 2)
    visibleMatrix = mm.current_generation[x - offset:x + offset, y - offset:y + offset]
    # print(visibleMatrix)


def locate_button_press():
    offset = round(cells_to_fit / 2)
    pos_x = mouse[0]
    pos_y = size_of_grid - mouse[1]  # inverted so that 0,0 is on top left (like matrix) instead of bottom left (graph)
    matrix_x = round((pos_x / cell_width) - 1/2)  # rounds to nearest cell number
    matrix_y = round((pos_y / cell_width) - 1/2)  # rounds to nearest cell number
    mm.current_generation[matrix_x - offset + matrix_x_position, matrix_y - offset + matrix_y_position] = \
            (not mm.current_generation[matrix_x -offset +matrix_x_position, matrix_y - offset + matrix_y_position]) * 1
                                                # flips the nearest
    # print(pos_x)
    # print(pos_y)
    # print(matrix_x)
    # print(matrix_y)


def draw_matrix():
    visible_matrix()
    live_cells = np.where(visibleMatrix == 1)
    # print(live_cells)
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
            graph.draw_line((0,size_of_grid - i * cell_width), (effective_grid_size,size_of_grid - i*cell_width))


def update_graph():
    graph.erase()
    draw_matrix()
    draw_grid()

def print_GUI_info():
    print('cell width: ' + str(cell_width))
    print('cells_to_fit: ' + str(cells_to_fit))
    print('grid_lines_status: ' + str(grid_lines))


def process_terminal():
    # print(mm.gen_saver)
    global grid_lines
    global cell_width
    global cells_to_fit
    if values['terminal'] == 'next':
        mm.next_generation()
        graph.erase()
        draw_matrix()
        draw_grid()
    if values['terminal'] == 'size up':
        cell_width += 1
        cells_to_fit = math.floor(size_of_grid / cell_width / 2) * 2
    if values['terminal'] == 'grid':
        grid_lines = not grid_lines
    if values['terminal'] == 'previous':
        if len(mm.gen_saver) != 0:
            mm.current_generation = mm.gen_saver[-1]
            mm.gen_saver.pop(-1)
    print('processed')



print_GUI_info()


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
        locate_button_press()
    if event == 'Okay':
        process_terminal()
    update_graph()