from sys import stdout
from math import floor, log10
from time import perf_counter as timer, sleep

def prompt_yes_no(prompt=' [Y/n] ', default=True):
    choice = input(prompt).lower()
    if choice in ('yes','y'):
        return True
    elif choice in ('no','n'):
        return False
    else:
        return default
    
def float_input():
    while True:
        var = input()
        try:
            val = float(var)
            return val
        except:
            print(f"{var} couldn't be converted to a float. Try again")


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
    
def print_data(data, end='\r',sigfigs=5):
    data_string =[]
    for d in data:
        if not isinstance(d,str):
            d = str(round_it(d,sigfigs))
        data_string.append(' '*(10-len(d))+d)
    print(','.join(data_string), end=end, flush=True)
    
def reset_cursor():
    """Reset the cursor in the terminal window."""
    stdout.write('\033[1;1H')


def clear_eol():
    """Clear all characters to the end of the line."""
    stdout.write('\x1b[2K')

def high_precision_sleep(duration):
    start_time = timer()
    while True:
        elapsed_time = timer() - start_time
        remaining_time = duration - elapsed_time
        if remaining_time <= 0:
            break
        if remaining_time > 0.02:  # Sleep for 5ms if remaining time is greater
            sleep(max(remaining_time/2, 0.0001))  # Sleep for the remaining time or minimum sleep interval
        else:
            pass

#***************************************************************************************
# https://esd.nasa.gov/now/nav/ui/classic/params/target/u_scan_assessed_cleared_list.do
    # %3Fsys_id%3D9d7a353f1b43e1549ad4cbb6624bcbf5
    # %3Fsys_id%3Da17ab53f1b43e1549ad4cbb6624bcb75
#***************************************************************************************
