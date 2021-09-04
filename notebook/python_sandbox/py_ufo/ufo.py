import os
import glob
import subprocess as sp
import time
import sys

import utils as uu

def run_me():
    
    drop_folder = os.path.join(uu.get_repos_root(), 'fortyfive', 'py_ufo', 'drops')
    

    sp.run(['python','--version'])
    
    run = True
    while run:

        py_scripts = glob.glob(os.path.join(drop_folder, r'*.py'))

        for s in py_scripts: 
            s_pth = os.path.join(drop_folder, s)
            out = sp.run(['python', s_pth])
            print(out)
        
        time.sleep(5)
        

        


if __name__ == '__main__':
    run_me()
