import tkinter as tk
from tkinter import ttk
from os import environ, system
from sys import platform as platform_
import time

from window_calibration import calibration, read_cal_file
from window_settings import settings, configuration
from daq_utils import config_first_detected_device
from data_utils import dataacq, Terminator2, get_path
from utils import print_data

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
    configuration.board = config_first_detected_device(use_dummy=True)

def run_daq():
    global run_name
    conf = configuration
    daq = conf.board
    header_keys = conf.header_keys
    local_time=time.ctime().replace(':','-').replace('  ',' ').replace(' ','_')
    output_filename = f"data/{conf.filename}_{local_time}.csv"
    out_file = get_path(output_filename)

    startseconds = time.time()   #  Get the start time in seconds

    dataavg = []
    datatime1 = time.time()
    term = Terminator2(conf.max_successive,conf.tol,conf.max_iter)
    s,z = read_cal_file(filename="cal.dat")

    with open(output_filename,'w') as output_file:
        output_file.write(local_time+'\n')
        output_file.write(run_name.get()+'\n')
        output_file.write(','.join(header_keys)+'\n')
        print_data(header_keys,'\n')
        try:
            while term.continue_reading:
                while not term:
                    #  function returns 5 seconds of averaged data for each channel in the dataavg[] array
                    data = [datatime1-startseconds,*dataacq(daq,z,s,conf.sample_rate,conf.sample_period)]
                    dataavg.append({key:val for key,val in zip(header_keys,data)})
                    output_file.write(','.join([str(d) for d in data])+'\n')
                    print_data(data)
                    datatime2 = time.time()
                    datatime1 = datatime2
                    term.check_var(data[1])
                term.reset()
                output_file.write('\n')
        except KeyboardInterrupt:
            pass
        except Exception as e:
            print('\n', e)
        finally:
            # Free the buffer in a finally block to prevent a memory leak.
            daq.release

def create_main_window():
    global run_name
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

    tab2.dispframe = tk.Frame(tab2,borderwidth=2,relief='groove')
    tab2.dispframe.pack()
    coming_soon = tk.Label(tab2.dispframe,text='Coming Soon')
    coming_soon.pack()
    calibration.add_data_row(self=tab2,data_set=[0]*4,title='')
    calibration.add_data_row(self=tab2,data_set=[0]*4,title='')
    return root

if __name__ == "__main__":
    root = create_main_window()
    root.mainloop()
