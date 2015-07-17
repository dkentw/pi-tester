import os

def pi_get_path(folder_name):
    '''Return the directory path under root directory of pi-tester
    '''
    root_dir = os.path.abspath(os.getcwd())
    pi_path = os.path.join(root_dir, folder_name)
    return pi_path
    
if __name__ == '__main__':
    #get_tools_dir()
    pass