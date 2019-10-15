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
    [PySimpleGUI.Text('Ставки main:', key='outcomes_label_main', font=('Calibri', 11), size=(30, 1), justification='left'),
     PySimpleGUI.Text('Ставки nextgoal:', key='outcomes_label_nextgoal', font=('Calibri', 11), size=(30, 1), justification='right')],
    [PySimpleGUI.Text('', key='main', font=('Calibri', 11), size=(30, 3), justification='left'),
     PySimpleGUI.Text('', key='nextgoal', font=('Calibri', 11), size=(30, 3), justification='right')],
    [PySimpleGUI.Combo(values=['Выбор матча'],
                       enable_events=True,
                       readonly=True,
                       key='topic_combobox',
                       auto_size_text=True,
                       size=(60, 3))]
]

# make window and a client for the server
window = PySimpleGUI.Window('Твои данные для матча v0.3', layout, grab_anywhere=False)
s = xmlrpc.client.ServerProxy(config['server_address'])


def write_to_file(path, bet, data_string):
    # write chosen bet types to a file
    try:
        with open(path % bet, 'w+') as bt:
            bt.write(data_string)
    except FileNotFoundError as e:
        PySimpleGUI.PopupError('Path does not exist: {e}'.format(e=e))
        sys.exit(1)


def request_outcomes(chosen_topic):
    # get bet types
    bet_types = []
    for topic in topics:
        bet_types.extend(s.return_bet_types(topic).split(','))

    # get outcomes for chosen topic and bet type
    outcomes_dict = {}
    for bet_type in bet_types:
        outcomes_dict[bet_type] = s.return_outcomes(chosen_topic, bet_type)
    return bet_types, outcomes_dict


while True:
    # request all topics available and put them in the combobox
    try:
        topics = s.return_all_topics().split(',')

        # load topics to UI
        window.Element('topic_combobox').Values = topics
    except ConnectionRefusedError as e:
        PySimpleGUI.PopupError('Server is not running: {e}'.format(e=e))
        sys.exit(1)

    # handle events, exit if done
    event, values = window.Read()
    if event in (None, 'Exit'):
        break

    elif event == 'topic_combobox':
        # get chosen bet type and topic from combobox
        chosen_topic = window.Element('topic_combobox').Get()

        # get outcomes for chosen topic and bet type
        bet_types, outcomes = request_outcomes(chosen_topic)

        for bet in bet_types:
            # show outcomes on their label
            window.Element(bet).Update(outcomes[bet])
            write_to_file(config['outcomes_file'], bet, outcomes[bet])
window.close()
