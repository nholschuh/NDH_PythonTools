def mpl_fix():
    """
    % (C) Nick Holschuh - Amherst College -- 2025 (Nick.Holschuh@gmail.com)
    %
    % This prints the string needed to make matplotlib use editable axes text
    %
    %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    """ 

    print('''
import matplotlib as mpl
mpl.rcParams['pdf.fonttype'] = 42  # Use TrueType fonts
mpl.rcParams['ps.fonttype'] = 42
''')
