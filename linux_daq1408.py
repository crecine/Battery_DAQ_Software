import uldaq
from uldaq import DaqDevice, ScanStatus



class daq1408:
    def __init__(self, device:DaqDevice, input_mode = uldaq.AiInputMode.SINGLE_ENDED):
        self.device = device.get_ai_device()
        device.connect(connection_code=0)
        self.board_num = 0
        self.input_mode = input_mode
        self._daq_device = device

    @property
    def ai_info(self):
        return self.device.get_info()
    @property
    def ai_range(self):
        return self.ai_info.get_ranges(self.input_mode)[0]
    @property
    def max_chan(self):
        return self.ai_info.get_num_chans_by_mode(self.input_mode)-1

    def analog_read(self, channel):
        return self.device.a_in(channel,self.input_mode,self.ai_range)

    def analog_scan(self,n_points_per_channel,rate, low_chan=0,high_chan=None):
        if high_chan is None:
            high_chan = self.max_chan
        n_channels = high_chan - low_chan +1

        aq_time = n_points_per_channel/rate
        data_buffer = uldaq.create_float_buffer(n_channels,n_points_per_channel)
        options = uldaq.ScanOption.DEFAULTIO
        flags = uldaq.AInScanFlag.NOSCALEDATA #should output counts instead of volts
        rate = self.device.a_in_scan(low_chan,high_chan,self.input_mode,self.ai_range,
                                n_points_per_channel,rate,options,flags,data_buffer)
        self.device.scan_wait(uldaq.WaitType.WAIT_UNTIL_DONE,aq_time*4)
        return data_buffer

    def release(self):
        status, transfer_status = self.device.get_scan_status()
        # Stop the acquisition if it is still running.
        if status == ScanStatus.RUNNING:
            self.device.scan_stop()
        if self._daq_device.is_connected():
            self._daq_device.disconnect()
        self._daq_device.release()