import tkinter as tk
from tkinter import ttk
from numpy import loadtxt
from os import listdir, environ, system, path as ospath
from sys import platform as platform_, path as syspath

from window_calibration import calibration
from window_settings import settings, configuration
from daq_utils import config_first_detected_device
from data_utils import dataacq

def setup(): #Set up
    environ['DISPLAY'] = ':0' #allow Cygwin to create GUI windows
    try:
        root = tk.Tk()
    except: 
        try:
            #run XLaunch if it hasn't been run yet
            if 'win' in platform_ and 'cyg' not in platform_:
                from os import startfile
                startfile("C:\\Program Files (x86)\\Xming\\XLaunch.exe")
            elif platform_ == 'cygwin':
                system('cygstart "C:/Program Files (x86)/Xming/XLaunch.exe"')
            else:
                print('X server failed to start. Please start manually and try again.')
                exit()
            input('Press Enter to continue...')
            root = tk.Tk()
        except:
            print('X server failed to start. Please start manually and try again.')
            exit()
    return root

def connect_daq():
    configuration.board = config_first_detected_device(0)

def run_daq():
    dataacq(configuration.board)

# if __name__ == "__main__":
root = setup()
root.geometry('400x475')
root.title('Battery DAQ Software - Carl Recine')

tabControl = ttk.Notebook(root)

tab1 = ttk.Frame(tabControl)
tab2 = ttk.Frame(tabControl)
tabControl.add(tab1, text='Record')
tabControl.add(tab2, text='Live View')
tabControl.pack(expand=1, fill="both")

button_frame = tk.Frame(tab1)
button_frame.pack(fill='x', side=tk.TOP)

cal_button = tk.Button(button_frame,text='Calibrate',command=calibration)
cal_button.pack(side = tk.LEFT)

sett_button = tk.Button(button_frame,text='Settings',command=settings)
sett_button.pack(side = tk.RIGHT)

input_frame = tk.Frame(tab1)
input_frame.pack()
run_label = tk.Label(input_frame,text='Run Name:')
run_name = tk.Entry(input_frame)
run_label.pack(side=tk.LEFT)
run_name.pack(side=tk.LEFT)

run_frame = tk.Frame(tab1)
run_frame.pack(side=tk.BOTTOM)
run_button = tk.Button(run_frame,text='Run',command=run_daq)
run_button.pack(side = tk.RIGHT)
connect_button = tk.Button(run_frame,text='Connect',command=connect_daq)
connect_button.pack(side = tk.RIGHT)

root.mainloop()