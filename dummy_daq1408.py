import numpy as np
from time import perf_counter as timer

from utils import high_precision_sleep

class daq1408:
    def __init__(self, device:int, input_mode = 'unused'):
        self.device = device
        self.board_num = device
        self.input_mode = input_mode
        self._use_ical = True

    class ai_info:
        supported_ranges = [10]
        num_chans = 8
    @property
    def ai_range(self):
        x = self.ai_info.supported_ranges[0]
        return (-x,x)
    @property
    def max_chan(self):
        return self.ai_info.num_chans-1
    
    def analog_read(self, channel):
        return np.random.uniform(-self.ai_info,self.ai_range)
    
    def analog_scan(self,n_points_per_channel,rate, low_chan=0,high_chan=None):
        t1 = timer()
        if high_chan is None:
            high_chan = self.max_chan
        n_channels = high_chan - low_chan +1
        runtime = n_points_per_channel/rate
        t2 = timer()
        high_precision_sleep(runtime-t2+t1)

        return np.random.uniform(*self.ai_range,n_points_per_channel*n_channels)




    def release(self):
        pass
