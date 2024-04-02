from data_utils import calibration, dataacq, Terminator2
from daq_utils import config_first_detected_device, daq1408

import time
import pandas as pd

#  NOTE: Current sensor hooked up to channel 0 and channels 1 to 7 will be voltage measurements with a 
#              voltage divider in place and so all channels will be calibrated. The same voltage will be applied to channels 1 to 7 during calibration.
header_keys = ['t','I','V1','V2','V3','V4','V5','V6','V7']

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
                                                     
# Acquire the battery test data.
print('\nPress enter to start data acquisition')
idat = input()

startseconds = time.time()   #  Get the start time in seconds

dataavg = []
datatime1 = time.time()
# trigger = {'num':0, 'max':3, 'tol':.0001}
term = Terminator2(max_successive=6,tol=.0001,max_iter=200)
# for ii in range(10): #20000
while not term:
    #  function returns 5 seconds of averaged data for each channel in the dataavg[] array
    data = [datatime1-startseconds,*dataacq(daq,z,s)]
    dataavg.append({key:val for key,val in zip(header_keys,data)})
    datatime2 = time.time()
    print(f'finished point {term.current_iter} in {datatime2-datatime1} seconds')
    datatime1 = datatime2
    term.check_var(data[1]*0)
    # if terminator(0,trigger):
    #     break

#  Get the time 
seconds = time.time() #  Get the current time in seconds
ellapseseconds = seconds-startseconds

# Write data to screen and to file
#time is in seconds and the dataavg[] values at in engineering units (Amps for channel 0 and Vdc for channels 1 through 7)
print("Total time:", ellapseseconds)
df = pd.DataFrame(dataavg)
print(df)

output_filename = f"data/test_results_{local_time}.csv"
df.to_csv(output_filename, index=False)
