Battery_DAQ_Software is a data aquisition software intended to be used with the Measurement Computing USB-1408FS-PLUS

This is designed to record voltage and current data while charging and discharging battery packs in various configurations, up to 7S.

battery_daq.py and gui.py can be run directly with Python. \
Utility functions are sorted into daq_utils, data_utils, gui_utils, and utils. \
windows_daq1408 and linux_daq1408 wrap important functions from their respective libraries into a common interface. \
dummy_daq1408 is also provided which allows for testing the software without an actual DAQ connected. \
The dummy daq has the same interface as the Linux and Windows versions, but will return randomly generated values when it is "read". \
The main window for the GUI can be created with create_main_window() in gui.py \
window_calibration and window_settings contain subclasses of tk.Tk that create and configure the windows when they are initialized. \
Terminator2 in data_utils can be used to end data collection early if certain trigger conditions are met.
