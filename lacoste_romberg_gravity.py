import numpy as np
import pandas as pd
import os

def lacoste_romberg_gravity(counter_vals):
    """
    % (C) Nick Holschuh - Amherst College - 2024 (Nick.Holschuh@gmail.com)
    %
    % 
    %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    % The inputs are as follows:
    %
    %
    %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    % The outputs are as follows:
    %
    %
    %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    """

    root_dir = os.path.dirname(os.path.abspath(__file__))
    lr_data = pd.read_excel(root_dir+'LacosteRomberg_Table.xlsx')
    y_interp = np.interp(counter_vals, lr_data['Counter Reading'], lr_data['Value'])

    return y_interp
