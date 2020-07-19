import numpy as np
import urllib.request
from map.library.orbital import Orbital
from abc import ABCMeta, abstractmethod
from map.config.config import config


class OrbitalData(Orbital):

    def __init__(self, cube, ID, name='', meta_data={}):

        self.name = name
        self.ID = ID
        self.meta_data = meta_data

        dk3D = float(config.get_key('orbital', 'dk3D'))

        super().__init__(cube, file_format='cube', dk3D=dk3D,
                         value='abs2')

    @classmethod
    def init_from_file(cls, file_path, ID):

        with open(file_path, 'r') as f:
            file = f.read()

            name, keys = OrbitalData._get_metadata(file, file_path)

        return cls(file, ID, name=name, meta_data=keys)

    @classmethod
    def _get_metadata(cls, file, file_path):

        first_line, second_line = file.split('\n')[:2]
        first_line = first_line.strip()
        second_line = second_line.strip()
        keys = {}

        if config.get_key('cube', 'line_one') == 'alias':
            name = first_line.strip()
            keys.update({config.get_key('cube', 'line_two'): second_line})

        elif config.get_key('cube', 'line_two') == 'alias':
            name = second_line.strip()
            keys.update({config.get_key('cube', 'line_one'): first_line})

        # File name without path and extension
        else:
            name = os.path.splitext(os.path.split(file_path)[1])[0]
            keys.update({config.get_key('cube', 'line_one'): first_line,
                         config.get_key('cube', 'line_two'): second_line})

        return name, keys

    @classmethod
    def init_from_online(cls, url, ID):

        with urllib.request.urlopen(url) as f:
            file = f.read().decode('utf-8')

            name, keys = OrbitalData._get_metadata(file, url)

        return cls(file, ID, name=name, meta_data=keys)
