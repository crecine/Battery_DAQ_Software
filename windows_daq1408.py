from mcculw import ul
from mcculw.enums import ScanOptions
from mcculw.device_info import DaqDeviceInfo
from ctypes import cast, POINTER, c_double, c_ushort, c_ulong

class daq1408:
    def __init__(self, device:int, input_mode = 'unused'):
        self.device = DaqDeviceInfo(device)
        self.board_num = device
        self.input_mode = input_mode

    @property
    def ai_info(self):
        return self.device.get_ai_info()
    @property
    def ai_range(self):
        return self.ai_info.supported_ranges[0]
    @property
    def max_chan(self):
        return self.ai_info.num_chans-1
    
    def analog_read(self, channel):
        return ul.a_in(self.board_num, channel, self.ai_range)
    
    def analog_scan(self,n_points_per_channel,rate, low_chan=0,high_chan=None):
        if high_chan is None:
            high_chan = self.max_chan
        n_channels = high_chan - low_chan +1

        n_points = n_points_per_channel*n_channels
        memhandle = ul.win_buf_alloc(n_points)
        data_buffer = cast(memhandle, POINTER(c_ushort))
        options = (ScanOptions.FOREGROUND)
        ul.a_in_scan(self.board_num,low_chan,high_chan,n_points,rate,
                        self.ai_range,memhandle,options)
        return data_buffer