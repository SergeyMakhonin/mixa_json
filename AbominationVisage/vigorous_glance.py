import sys

import PySimpleGUI
import xmlrpc.client
from logging_and_configuration import json_reader

try:
    config = json_reader('config.json')
except FileNotFoundError as e:
    PySimpleGUI.PopupError('Config not found: {e}'.format(e=e))
    sys.exit(1)

layout = [
    [PySimpleGUI.Text('Outcomes:\n', font=('Calibri', 11), size=(30, 1), justification='left')],
    [PySimpleGUI.Text('No data', key='outcomes', font=('Calibri', 11), size=(30, 3))],
    [PySimpleGUI.Combo(values=['no data'],
                       enable_events=True,
                       readonly=True,
                       key='topic_combobox',
                       auto_size_text=True,
                       size=(30, 3))],
    [PySimpleGUI.Combo(values=['no data'],
                       enable_events=True,
                       readonly=True,
                       key='bet_types_combobox',
                       auto_size_text=True,
                       size=(30, 3))]
]

# make window and a client for the server
window = PySimpleGUI.Window('Client', layout, grab_anywhere=False)
s = xmlrpc.client.ServerProxy(config['server_address'])


def write_to_file(path, data_string):
    # write chosen bet types to a file
    try:
        with open(path, 'w+') as bt:
            bt.write(data_string)
    except FileNotFoundError as e:
        PySimpleGUI.PopupError('Path does not exist: {e}'.format(e=e))
        sys.exit(1)


while True:
    # request all topics available and put them in the combobox
    try:
        topics = s.return_all_topics().split(',')
        bet_types = []
        for topic in topics:
            bet_types.extend(s.return_bet_types(topic).split(','))

        # load topics to UI
        window.Element('topic_combobox').Values = topics
        window.Element('bet_types_combobox').Values = bet_types
    except ConnectionRefusedError as e:
        PySimpleGUI.PopupError('Server is not running: {e}'.format(e=e))
        sys.exit(1)

    # handle events, exit if done
    event, values = window.Read()
    if event in (None, 'Exit'):
        break

    elif event == 'bet_types_combobox':
        # get chosen bet type and topic from combobox
        chosen_topic = window.Element('topic_combobox').Get()
        chosen_bet_type = window.Element('bet_types_combobox').Get()

        # get outcomes for chosen topic and bet type
        outcomes = s.return_outcomes(chosen_topic, chosen_bet_type)

        # show outcomes on their label
        window.Finalize()
        window.Element('outcomes').Update(outcomes)

        write_to_file(config['outcomes_file'], outcomes)
window.close()
