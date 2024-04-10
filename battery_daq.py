from data_utils import calibration, dataacq, Terminator2
from daq_utils import config_first_detected_device
from utils import prompt_yes_no, print_data
from pathlib import Path

import time
import pandas as pd

#  NOTE: Current sensor hooked up to channel 0 and channels 1 to 7 will be voltage measurements with a 
#              voltage divider in place and so all channels will be calibrated. The same voltage will be applied to channels 1 to 7 during calibration.
header_keys = ['t','I','V1','V2','V3','V4','V5','V6','V7']

# time and date stamp the csv data file
local_time=time.ctime().replace(':','-').replace('  ',' ').replace(' ','_')
print("local time:",local_time)
output_filename = f"data/test_results_{local_time}.csv"
out_file = Path(output_filename)
if not out_file.parent.exists():
    out_file.parent.mkdir(parents=True, exist_ok=True)

# configure first detected device as board number 0
daq = config_first_detected_device(0)

print(' Read calibration data from cal.dat file? ')
read_cal = prompt_yes_no() #True to use stored calibration, False to calibrate now
#  function returns calibration coefficients zero array (z[]) and span array (s[]) for channels 0-7
z, s = calibration(daq, read_cal)

print('\nEnter run/configuration name: ')
run_name = input()

# Acquire the battery test data.
idat = input('\nPress enter to start data acquisition:')
print('Starting Acquisition')

startseconds = time.time()   #  Get the start time in seconds

dataavg = []
datatime1 = time.time()
term = Terminator2(max_successive=12,tol=.05,max_iter=20000)

with open(output_filename,'w') as output_file:
    output_file.write(local_time+'\n')
    output_file.write(run_name+'\n')
    output_file.write(','.join(header_keys)+'\n')
    print_data(header_keys,'\n')
    try:
        while term.continue_reading:
            while not term:
                #  function returns 5 seconds of averaged data for each channel in the dataavg[] array
                data = [datatime1-startseconds,*dataacq(daq,z,s)]
                dataavg.append({key:val for key,val in zip(header_keys,data)})
                output_file.write(','.join([str(d) for d in data])+'\n')
                print_data(data)
                datatime2 = time.time()
                # print(f'finished point {term.current_iter} in {datatime2-datatime1} seconds')
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


#  Get the time 
seconds = time.time() #  Get the current time in seconds
ellapseseconds = seconds-startseconds

# Write data to screen and to file
#time is in seconds and the dataavg[] values at in engineering units (Amps for channel 0 and Vdc for channels 1 through 7)
print("Total time:", ellapseseconds)
df = pd.DataFrame(dataavg)
print(df)


# df.to_csv(output_filename, index=False)
