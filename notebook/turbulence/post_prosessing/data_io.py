import os, sys, shutil
import time
from typing import Dict
import numpy as np
import json

def _clean_folder(folder):
    if os.path.exists(folder):
        shutil.rmtree(folder)
    time.sleep(0.5)
    os.makedirs(folder, exist_ok=True)


class DataIO:

    def __init__(self, root_folder):
        self.root_folder = root_folder
        self.data_folder = os.path.join(root_folder, 'data')
        self.fig_folder = os.path.join(root_folder, 'fig')

    def clean_all(self):
        self.clean_data()
        self.clean_fig()
    
    def clean_data(self):
        _clean_folder(self.data_folder)

    def clean_fig(self):
        _clean_folder(self.fig_folder)
    
    def save_data(self, file_name_wo_ext: str, data: np.array, kw_attribs: Dict = {}):
        np.save(os.path.join(self.data_folder, file_name_wo_ext + '.npy'), data)
        att_file = os.path.join(self.data_folder, file_name_wo_ext + '.json')
        with open(att_file, 'w') as out_f:
            json.dump(kw_attribs, out_f)

    def read_data(self, file_name_wo_ext: str):
        data_fn = os.path.join(self.data_folder, file_name_wo_ext)
        mtx_data = np.load(data_fn + '.npy')
    
        with open(data_fn + '.json', 'r') as in_f:
            kw_attribs = json.load(in_f)

        return mtx_data, kw_attribs




