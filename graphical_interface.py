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
run_once = True

matrix_x_position = round(mm.matrix_size/2)
matrix_y_position = round(mm.matrix_size/2)

# GUI initialization

sg.theme('LightGreen2')  # background color

layout = [[sg.Graph((size_of_grid, size_of_grid), (0, 0), (size_of_grid, size_of_grid), key='GRAPH',
                    change_submits=True, drag_submits=False)],
          [sg.Text('Enter command:'), sg.InputText(key='terminal')],
          [sg.Button('Okay'), sg.Cancel()]]

window = sg.Window('My new window', return_keyboard_events=True, use_default_focus=False).Layout(layout)
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
    matrix_x = round((pos_x / cell_width) - 1 / 2)  # rounds to nearest cell number
    matrix_y = round((pos_y / cell_width) - 1 / 2)  # rounds to nearest cell number
    mm.current_generation[matrix_x - offset + matrix_x_position, matrix_y - offset + matrix_y_position] = \
        (not mm.current_generation[matrix_x - offset + matrix_x_position, matrix_y - offset + matrix_y_position]) * 1
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
        matrix_y_position -= round(96/cell_width)
    elif direction == 'Down':
        matrix_y_position += round(96/cell_width)
    elif direction == 'Right':
        matrix_x_position += round(96/cell_width)
    elif direction == 'Left':
        matrix_x_position -= round(96/cell_width)
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
    if ';'in event:
        if len(mm.gen_saver) != 0:
            mm.current_generation = mm.gen_saver[-1]
            mm.gen_saver.pop(-1)
    if '\'' in event:
        mm.current_generation = mm.next_generation(mm.current_generation)


def process_terminal():
    # print(mm.gen_saver)
    global grid_lines
    global cell_width
    global cells_to_fit
    if values['terminal'] == 'next':
        mm.current_generation = mm.next_generation(mm.current_generation)
        graph.erase()
        draw_matrix()
        draw_grid()
    elif values['terminal'] == 'size up':
        cell_width += 1
        cells_to_fit = math.floor(size_of_grid / cell_width / 2) * 2
    elif values['terminal'] == 'grid':
        grid_lines = not grid_lines
    elif values['terminal'] == 'previous':
        if len(mm.gen_saver) != 0:
            mm.current_generation = mm.gen_saver[-1]
            mm.gen_saver.pop(-1)
    elif values['terminal'] == 'diag':
        print_GUI_info()
    elif values['terminal'] == 'clear':
        mm.current_generation = np.zeros((mm.matrix_size, mm.matrix_size))
    else:
        navigate(values['terminal'])
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
    keypress_check()
    update_graph()