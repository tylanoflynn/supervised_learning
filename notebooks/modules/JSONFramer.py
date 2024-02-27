import pandas as pd
import numpy as np
import os
import json

class JSONFramer:
    def __init__(self, dir, keys):
        self.directory = dir
        self.keys = keys

    def _get_nested_value(self, data):
        try:
            for key in self.keys:
                data = data[key]
            return data
        except (TypeError, KeyError):
            return None
        
    