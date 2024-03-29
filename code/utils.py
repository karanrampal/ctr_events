#!/usr/bin/env python3
"""Utility functions and classes
"""

import json
import logging
import os


class Params():
    """Class to load hyperparameters from a json file.
    """

    def __init__(self, json_path):
        with open(json_path) as f:
            params = json.load(f)
            self.__dict__.update(params)

    def save(self, json_path):
        """Save parameters to json file at json_path
        """
        with open(json_path, 'w') as f:
            json.dump(self.__dict__, f, indent=4)


class RunningAverage():
    """A class that maintains the running average of a quantity
    """
    def __init__(self):
        self.steps = 0
        self.total = 0

    def update(self, val):
        """Update step count and value of the variable
        """
        self.total += val
        self.steps += 1

    def __call__(self):
        return self.total/float(self.steps)


def set_logger(log_path):
    """Set the logger to log info in terminal and file at log_path.
    Args:
        log_path: (string) location of log file
    """
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)

    if not logger.handlers:
        # Logging to a file
        file_handler = logging.FileHandler(log_path, mode='w')
        file_handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s: %(message)s'))
        logger.addHandler(file_handler)

        # Logging to console
        stream_handler = logging.StreamHandler()
        stream_handler.setFormatter(logging.Formatter('%(message)s'))
        logger.addHandler(stream_handler)


def save_dict_to_json(data, json_path):
    """Saves a dict of floats to json file
    Args:
        data: (dict) of float-castable values (np.float, int, float, etc.)
        json_path: (string) path to json file
    """
    with open(json_path, 'w') as f:
        data = {k: float(v) for k, v in data.items()}
        json.dump(data, f, indent=4)


def safe_makedir(path):
    """Make directory given the path if it doesn't already exist
    Args:
        path: path of the directory to be made
    """
    if not os.path.exists(path):
        os.makedirs(path)
