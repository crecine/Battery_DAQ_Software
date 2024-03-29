from numpy import loadtxt
from daq_utils import daq1408

def calibration(board:daq1408, ical=1):
    if ical==1:           # calibrate
        # Open a file to write calibration coefficients, prompt responses and averaged data from all channels
        print("\nSet a low signal to all channels and press enter to take calibration point: ", end=" ")
        input()

        dataavglow = dataacq(board)     # Acquire the low voltage calibration data

        print("\nEnter current in Amps set on channel 0: ", end=" ")
        curlow = float(input())

        print("\nEnter voltage in set on channels 1 through 7: ", end=" ")
        voltlow = float(input())

        print("\nSet a high signal to all channels and press enter to take calibration point: ", end=" ")
        input()

        dataavghigh = dataacq(board)     # Acquire the high voltage calibration data     

        print("\nEnter current in Amps set on channel 0: ", end=" ")
        curhigh = float(input())

        print("\nEnter voltage in set on channels 1 through 7: ", end=" ")
        volthigh = float(input())

    #  Compute the calibration coefficients for each channel assuming linearity ( measurement in engineering units = s[i]*counts+z[i] )
        s, z = [0]*8, [0]*8
        s[0]=(curhigh-curlow)/(dataavghigh[0]- dataavglow[0])
        z[0]=curhigh-s[0]* dataavghigh[0]

        for i in range(1,8):
            s[i]= (volthigh-voltlow)/(dataavghigh[i]- dataavglow[i])
            z[i] = volthigh-s[i]* dataavghigh[i]
        
        with open('cal.dat', 'w') as output_file:
            output_file.write(str(s).strip('[]'))
            output_file.write('\n')
            output_file.write(str(z).strip('[]'))


    elif ical==2:        # read arrays z and s from disk file
        lines = loadtxt("cal.dat", comments="#", delimiter=",", unpack=False)
        print(lines)
        [s,z] = lines

    print("\nThe calibration zeros are : ", end=" ")
    for i in range(0,8):
        print(z[i], end=" ")

    print("\nThe calibration span values are : ", end=" ")
    for i in range(0,8):
        print(s[i], end=" ")

    return z, s

#***************************************************************************************

def dataacq(board:daq1408, zeros=None, spans=None, sample_rate=10):   
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
    sample_rate = 10             # (hz) sample frequency for each channel
    sample_period = 5            # (s) sample period

    # Acquire data buffer ibuf[] of size ibuflength from A-D.
    n_points_per_chan = sample_period * sample_rate
    ibuf = board.analog_scan(n_points_per_chan,sample_rate)

    # Average buffer data for each channel to get icountavg[].
    countavg = [0]*numchan
    for ii in range(numchan):
        for jj in range(sample_period*sample_rate):
            m = jj + ii*numchan
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
# https://esd.nasa.gov/now/nav/ui/classic/params/target/u_scan_assessed_cleared_list.do
    # %3Fsys_id%3D9d7a353f1b43e1549ad4cbb6624bcbf5
    # %3Fsys_id%3Da17ab53f1b43e1549ad4cbb6624bcb75
#***************************************************************************************
