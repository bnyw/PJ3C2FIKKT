import PySimpleGUI as sg
    
layout = [
    [
        sg.Graph(
            canvas_size=(400, 400),
            graph_bottom_left=(0, 400),
            graph_top_right=(400, 0),
            key="graph",
            change_submits=True,

            # enabling drag_submits enables mouse_drags, but disables mouse_up events
            drag_submits=True 
        )
    ]
]

window = sg.Window("mouse events" , layout, size=(400,400))
window.Finalize()

graph = window.Element("graph")

click = False

while True:
    event, values = window.Read()
    if event is None:
        break # exit

    if event == "graph" and not click:
        click = True
        print("DOWN",values["graph"])
    
    if event == "graph+UP" and click: 
        click = False
        print("UP",values["graph"])