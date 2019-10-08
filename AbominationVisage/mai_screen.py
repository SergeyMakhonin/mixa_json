import PySimpleGUI

layout = [
    [PySimpleGUI.Text('This is input field', font=('Calibri', 11), size=(30, 1), justification='left')],
    [PySimpleGUI.InputText("write something...", font=('Calibri', 11), size=(30, 1))],
    [PySimpleGUI.Combo(values=('Listbox 1', 'Listbox 2', 'Listbox 3'), size=(30, 3))]
]

window = PySimpleGUI.Window('Client', layout, grab_anywhere=False)

event, values = window.Read()

