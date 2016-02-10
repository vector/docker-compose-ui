"""
find docker-compose.yml files
"""

import os

def find_yml_files(path):
    """
    find docker-compose.yml files in path
    """
    matches = {}
    for item in os.listdir(path):
        print os.path.join(path, item, 'docker-compose.yml')
        if os.path.isfile(os.path.join(path, item, 'docker-compose.yml')):
            matches[item] = os.path.join(path, item)
    return matches
