from sys import stdout
from math import floor, log10

def prompt_yes_no(prompt=' [Y/n] ', default=True):
    choice = input(prompt).lower()
    if choice in ('yes','y'):
        return True
    elif choice in ('no','n'):
        return False
    else:
        return default
    
def round_it(x, sig=None):
    # default sig figs to 2 decimal places out
    if isinstance(x, str):
        try:
            x = float(x)
        except ValueError:
            return x
    if not sig:
        sig = len(str(round(x)))+2
    if x != 0:
        return round(x, sig-int(floor(log10(abs(x))))-1)
    else:
        return 0
    
def print_data(data, end='\r'):
    data_string =[]
    for d in data:
        if not isinstance(d,str):
            d = str(round_it(d,5))
        data_string.append(' '*(8-len(d))+d)
    print(','.join(data_string), end=end, flush=True)
    
def reset_cursor():
    """Reset the cursor in the terminal window."""
    stdout.write('\033[1;1H')


def clear_eol():
    """Clear all characters to the end of the line."""
    stdout.write('\x1b[2K')

#***************************************************************************************
# https://esd.nasa.gov/now/nav/ui/classic/params/target/u_scan_assessed_cleared_list.do
    # %3Fsys_id%3D9d7a353f1b43e1549ad4cbb6624bcbf5
    # %3Fsys_id%3Da17ab53f1b43e1549ad4cbb6624bcb75
#***************************************************************************************
