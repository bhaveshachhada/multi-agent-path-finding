import os
import json


def load_json(filename=''):
    if not os.path.exists(filename):
        print(f'Graph file: {filename} does not exist')
        return None
    with open(filename, 'r') as graph_file:
        data = json.load(graph_file)
    return data
