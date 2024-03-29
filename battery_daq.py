from data_utils import calibration, dataacq
from daq_utils import config_first_detected_device, daq1408

import time
import pandas as pd

#  NOTE: Current sensor hooked up to channel 0 and channels 1 to 7 will be voltage measurements with a 
#              voltage divider in place and so all channels will be calibrated. The same voltage will be applied to channels 1 to 7 during calibration.
channel_keys = ['I','V1','V2','V3','V4','V5','V6','V7']

# time and date stamp the csv data file
local_time=time.ctime().replace(':','-').replace(' ','_')
print("local time:",local_time)

# configure first detected device as board number 1
board = config_first_detected_device(1)
daq = daq1408(board)

print(' Enter 1 to calibrate or 2 (default) to read calibration data from cal.dat file ')
ical = input()
ical = int(ical) if ical!='' else 2
#  function returns calibration coefficients zero array (z[]) and span array (s[]) for channels 0-7
z, s = calibration(daq, ical)

with open(f"data/test_results_{local_time}.csv","w") as results_file:
                                                     
    # Acquire the battery test data.
    print('\nPress enter to start data acquisition')
    idat = input()

    startseconds = time.time()   #  Get the start time in seconds

    dataavg = []
    datatime1 = time.time()
    for ii in range(10): #20000
        data = dataacq(daq,z,s)
        data_set = {'t':datatime1-startseconds}
        data_set.update({key:val for key,val in zip(channel_keys,data)})
        dataavg.append(data_set) #  function returns 5 seconds of averaged data for each channel in the dataavg[] array
        datatime2 = time.time()
        print(f'finished point {ii} in {datatime2-datatime1} seconds')
        datatime1 = datatime2

    #  Get the time 
    seconds = time.time() #  Get the current time in seconds
    ellapseseconds = seconds-startseconds

    # Write data to screen and to file
    #time is in seconds and the dataavg[] values at in engineering units (Amps for channel 0 and Vdc for channels 1 through 7)
    print("Total time:", ellapseseconds)
    df = pd.DataFrame(dataavg)
    print(df)

    results_file.write(str(ellapseseconds))
    for data in dataavg:
        results_file.write('\n')
        results_file.write(str(data))


    # Terminate data acquisition criteria 



# data_set = []
# for input_data in input_data_sets:
#     output_data = output.asdict()
#     data_set.append({**input_data, **output_data})

# df = pd.DataFrame(data_set).fillna(0)
# print(df)