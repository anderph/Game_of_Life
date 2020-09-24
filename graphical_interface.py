# This is the Graphical Interface file.
#
# Here, I will allow the user to see the grid, change the grid size, go forward and back generations


import PySimpleGUI as sg

sg.theme('DarkAmber')   # Add a little color to your windows

layout = [ [sg.Text('Test For GUI')],
           [sg.Graph((400,400), (0,0), (400,400), key='GRAPH')],
           [sg.Text('Enter command:'), sg.InputText()],
           [sg.OK(), sg.Cancel()]]

window = sg.Window('My new window').Layout(layout)
graph = window.Element('GRAPH')


event, values = window.Read()


while True:             # Event Loop
    event, values = window.Read()
    if event is None:
        break
    for i in range(1,10):
        top_left = (i*25, i*25)
        bot_right = (i*25+20, i*25-20)
        graph.DrawRectangle(top_left, bot_right, fill_color='red', line_color='red')
