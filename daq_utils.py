from sys import platform
from utils import prompt_yes_no
if platform.startswith('win'):
    from mcculw import ul
    from mcculw.enums import InterfaceType
    from windows_daq1408 import daq1408
else:
    import uldaq
    from uldaq import InterfaceType, DaqDevice
    from linux_daq1408 import daq1408


def config_first_detected_device(board_num=0, dev_id_list=None):
    """
    For Windows, this will return the board_number, for Linux it will return a DaqDevice.
    In either case, the result will be passed directly to daq1408() to initialize it.

    Adapted from mcculw/examples/console/console_examples_util.py
    Adds the first available device to the UL.  If a types_list is specified,
    the first available device in the types list will be add to the UL.

    Parameters
    ----------
    board_num : int
        The board number to assign to the board when configuring the device.

    dev_id_list : list[int], optional
        A list of product IDs used to filter the results. Default is None.
        See UL documentation for device IDs.
    """
    if platform.startswith('win'):
        print(' Windows detected, use InstaCal configuration? ')
        use_ical = prompt_yes_no()
        if not use_ical:
            ul.ignore_instacal()
        devices = ul.get_daq_device_inventory(InterfaceType.ANY)
    else:
        devices = uldaq.get_daq_device_inventory(InterfaceType.ANY)

    if not devices:
        raise Exception('Error: No DAQ devices found')

    print('Found', len(devices), 'DAQ device(s):')
    for device in devices:
        print('  ', device.product_name, ' (', device.unique_id, ') - ',
              'Device ID = ', device.product_id, sep='')

    device = devices[board_num]
    if dev_id_list:
        device = next((device for device in devices
                       if device.product_id in dev_id_list), None)
        if not device:
            err_str = 'Error: No DAQ device found in device ID list: '
            err_str += ','.join(str(dev_id) for dev_id in dev_id_list)
            raise Exception(err_str)
        
    print('Using:  ', device.product_name, ' (', device.unique_id, ') - ',
            'Device ID = ', device.product_id, sep='')

    if platform.startswith('win'):
        # Add the first DAQ device to the UL with the specified board number
        if not use_ical:
            ul.create_daq_device(board_num, device)
        daq = daq1408(board_num)
        daq._use_ical = use_ical
        return daq
    else:
        daq = daq1408(DaqDevice(device))
        return daq
