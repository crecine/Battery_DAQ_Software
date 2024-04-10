from numpy import loadtxt
from pathlib import Path

from daq_utils import daq1408
from utils import prompt_yes_no, round_it, float_input

def calibration(board:daq1408, read_cal=False):
    if not read_cal:           # calibrate
        # Open a file to write calibration coefficients, prompt responses and averaged data from all channels
        print("\nSet a low signal to all channels and press enter: ", end=" ")
        input()

        print("\nEnter voltage in Volts set on channels 1 through 7: ", end=" ")
        voltlow = float_input()
        low_voltage = dataacq(board)     # Acquire the low voltage calibration data

        print("\nEnter current in Amps set on channel 0: ", end=" ")
        curlow = float_input()
        low_current = dataacq(board)     # Acquire the low current calibration data

        print("\nSet a high signal to all channels and press enter: ", end=" ")
        input()

        print("\nEnter voltage in Volts set on channels 1 through 7: ", end=" ")
        volthigh = float_input()
        high_voltage = dataacq(board)     # Acquire the high voltage calibration data   
 
        print("\nEnter current in Amps set on channel 0: ", end=" ")
        curhigh = float_input()
        high_current = dataacq(board)     # Acquire the high current calibration data

        dataavglow = [low_current[0],*low_voltage[1:]]
        dataavghigh = [high_current[0],*high_voltage[1:]]

    #  Compute the calibration coefficients for each channel assuming linearity ( measurement in engineering units = s[i]*counts+z[i] )
        s, z = [0]*8, [0]*8
        print(dataavghigh)
        print(dataavglow)
        s[0]=(curhigh-curlow)/(dataavghigh[0]- dataavglow[0])
        z[0]=curhigh-s[0]* dataavghigh[0]

        for i in range(1,len(dataavghigh)):
            s[i]= (volthigh-voltlow)/(dataavghigh[i]- dataavglow[i])
            z[i] = volthigh-s[i]* dataavghigh[i]
        
        with open('cal.dat', 'w') as output_file:
            output_file.write(str(s).strip('[]'))
            output_file.write('\n')
            output_file.write(str(z).strip('[]'))


    else:        # read arrays z and s from disk file
        lines = loadtxt("cal.dat", comments="#", delimiter=",", unpack=False)
        print(lines)
        [s,z] = lines

    print("\nThe calibration zeros are : ", end=" ")
    for i in range(0,8):
        print(round(z[i],5), end=" ")

    print("\nThe calibration span values are : ", end=" ")
    for i in range(0,8):
        print(round(s[i],5), end=" ")
    print()

    return z, s

#***************************************************************************************

def dataacq(board:daq1408, zeros=None, spans=None, sample_rate=200, sample_period=5):   
    '''
    collect 5 seconds of data, average the data and apply the calibration for each channel
    if zeros and spans are not specified, they will default to 0 and 1
    sample rate is specified in hz
    '''

#   Measurement Computing USB-1408FS-Plus A/D board
#        board is 13 bit in single-ended mode, 8 channels total
#        1 count =  (10 V - -10 V)/2^13 = 0.00244140625 V but we may have voltage dividers so each channel is calibrated

#  Channel 0 is the current measurement (hall effect sensor)
#  Channels 1 to 7 are battery voltage measurements 

    numchan = board.max_chan+1  #  total number of channels to scan

    # Acquire data buffer ibuf[] of size ibuflength from A-D.
    n_points_per_chan = sample_period * sample_rate
    ibuf = board.analog_scan(n_points_per_chan,sample_rate)

    # Average buffer data for each channel to get icountavg[].
    countavg = [0]*numchan
    for ii in range(numchan):
        for jj in range(sample_period*sample_rate):
            m = ii + jj*numchan
            countavg[ii] += ibuf[m]
        countavg[ii] /= n_points_per_chan

    # Apply the calibration for each channel ( measurement in engineering units = s[i]*counts+z[i] )
    if zeros is None:
        zeros = [0]*numchan
    if spans is None:
        spans = [1]*numchan

    dataavg = [s*avg+z for (avg,z,s) in zip(countavg,zeros,spans)]

    return dataavg

#***************************************************************************************

def terminator(val, trigger):
    if abs(val) < trigger['tol']:
        trigger['num']+=1
    else:
        trigger['num']=0
    if trigger['num'] > trigger['max']:
        return True
    else:
        return False
    
class Terminator2:
    def __init__(self, max_successive=5, tol=.0001, max_iter=20000):
        self.check_num = 0
        self.max_successive = max_successive
        self.tol = tol
        self.current_iter = 0
        self.max_iter = max_iter
        self.continue_reading = True

    def check_var(self,val):
        self.current_iter += 1
        if abs(val) < self.tol:
            self.check_num+=1
        else:
            self.check_num=0
    
    def reset(self):
        print('\nContinue Reading?')
        self.continue_reading = prompt_yes_no(' [y/N] ', default=False)
        self.check_num = 0
    
    def __bool__(self):
        if self.check_num > self.max_successive:
            print('\n\nTerminating due to trigger condition')
            return True
        elif self.current_iter > self.max_iter:
            print('\n\nMaximum iterations reached')
            return True
        else:
            return False
    __nonzero__=__bool__

def get_path(file_name:str):
    out_file = Path(file_name)
    if not out_file.parent.exists():
        out_file.parent.mkdir(parents=True, exist_ok=True)
    return out_file
