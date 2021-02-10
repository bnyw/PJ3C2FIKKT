import PySimpleGUI as sg
import matplotlib.pyplot as plt
from PIL import Image
from math import floor
import io
import base64
# import yoloooo

# Set window's theme
sg.theme('TealMono')

# Define custom function for working with image
def ctb(file_or_bytes, resize=None):
    '''
    Will convert into bytes and optionally resize an image that is a file or a base64 bytes object.
    Turns into  PNG format in the process so that can be displayed by tkinter
    :param file_or_bytes: either a string filename or a bytes base64 image object
    :type file_or_bytes:  (Union[str, bytes])
    :param resize:  optional new size
    :type resize: (Tuple[int, int] or None)
    :return: (bytes) a byte-string object
    :rtype: (bytes)
    '''
    if isinstance(file_or_bytes, str):
        img = Image.open(file_or_bytes)
    else:
        try:
            img = Image.open(io.BytesIO(base64.b64decode(file_or_bytes)))
        except Exception as e:
            dataBytesIO = io.BytesIO(file_or_bytes)
            img = Image.open(dataBytesIO)

    cur_width, cur_height = img.size
    if resize:
        new_width, new_height = resize
        scale = min(new_height/cur_height, new_width/cur_width)
        img = img.resize((int(cur_width*scale), int(cur_height*scale)), Image.ANTIALIAS)
    bio = io.BytesIO()
    img.save(bio, format="PNG")
    del img
    return bio.getvalue()

# Define the window's contents
layout = [[sg.Slider(range=(1,0),
                    default_value=0.5,
                    resolution=0.001,
                    orientation='v',
                    key='-slider_one-',
                    size=(23,20),
                    enable_events=True),

            # sg.Image(data=ctb('car5crop1.jpg',(600,400)),key='-IMAGE-'),

            sg.Graph(canvas_size=(600, 400),
                    graph_bottom_left=(0, 400),
                    graph_top_right=(600, 0),
                    key="graph",
                    enable_events=True,
                    drag_submits=True),

            sg.Slider(range=(1,0),
                    default_value=0.5,
                    resolution=0.001,
                    orientation='v',
                    key='-slider_two-',
                    size=(23,20),
                    enable_events=True)],

        [sg.Button('Commit change',size=(15,1),key='-commit-'),
            sg.Checkbox('Frame',enable_events=True,key='-frame-')],

        [sg.Button('Run',size=(15,1),disabled=True,key='-run-'),
            sg.Checkbox('Image pass-through',disabled=True,key='-image_pass-'),
            sg.Checkbox('Performance monitoring',disabled=True,key='-perf_monitor-'),
            sg.Text(size=(25,1),key='-perf_text-')],

        [sg.Button('Visualize',size=(15,1),disabled=True,key='-visualize-')]]

# Create the window
window = sg.Window('Test', layout)

window.Finalize()

graph = window.Element("graph")

graph.draw_image(data = ctb('car5crop1.jpg',(600,400)),location = (0,0))

# Display and interact with the Window using an Event Loop
while True:
    event, values = window.read()

    y1 = floor(values['-slider_one-']*400)
    y2 = floor(values['-slider_two-']*400)

    # See if window was closed
    if event == sg.WINDOW_CLOSED:
        break

    if event == '-frame-':
        if values['-frame-']:
            frame = []
            for i in range(6):
                # frame.append(graph.draw_line((600*i/5,0),(600*i/5,400), color='red', width = 5))
                frame.append(graph.draw_rectangle((600*i/5,y1),(600*i/5,y2), line_color='red', line_width = 5))
        else:
            try:
                for id in frame:
                    graph.delete_figure(id)
            except:
                pass

    if event == '-commit-':
        if values['-slider_one-'] == values['-slider_two-']:
            sg.popup_error("Two slider can't be same number",title="Error")
            continue
        
        window['-run-'].update(disabled=False)
        window['-image_pass-'].update(disabled=False)
        window['-perf_monitor-'].update(disabled=False)
        window['-perf_text-'].update('')
        window['-commit-'].update(disabled=True)

    if event == '-run-':
        fTop = min(y1,y2)
        fBottom = max(y1,y2)

        if values['-image_pass-']:
            result,Available,perf_mon = yoloooo.app(5,fTop,fBottom,grid_img)
        else:
            result,Available,perf_mon = yoloooo.app(5,fTop,fBottom)
        
        if values['-perf_monitor-']:
            update_text = 'Processing time : ' + str(perf_mon)
            window['-perf_text-'].update(update_text)

        window['-visualize-'].update(disabled=False)
        # print(Available)

    if event == '-visualize-':
        plt.imshow(result)
        plt.show(block=False)

    if event == '-slider_one-' or event == '-slider_two-':
        try:
            for id in line:
                graph.delete_figure(id)
            for id in frame:
                graph.delete_figure(id)
        except:
            pass

        line = []
        line.append(graph.draw_line((0,y1),(600,y1), color='red', width = 5))
        line.append(graph.draw_line((0,y2),(600,y2), color='red', width = 5))

        if values['-frame-']:
            frame = []
            for i in range(6):
                # frame.append(graph.draw_line((600*i/5,0),(600*i/5,400), color='red', width = 5))
                frame.append(graph.draw_rectangle((600*i/5,y1),(600*i/5,y2), line_color='red', line_width = 5))
        else:
            try:
                for id in frame:
                    graph.delete_figure(id)
            except:
                pass
        
        window['-run-'].update(disabled=True)
        window['-image_pass-'].update(disabled=True)
        window['-perf_monitor-'].update(disabled=True)
        window['-commit-'].update(disabled=False)
        window['-visualize-'].update(disabled=True)

# Finish up by removing from the screen
window.close()