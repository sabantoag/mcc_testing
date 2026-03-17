from mcculw.device_info import DaqDeviceInfo
from mcculw import ul


def measure_voltage(daq_device: DaqDeviceInfo, channel: int) -> float:
    """Return the measured voltage value from a 16 bit resolution analog input channel.

    Args:
        daq_device (DaqDeviceInfo): DAQ device information object.
        channel (int): The channel number to read from.

    Returns:
        float: The measured voltage in engineering units.
    """
    # Read the input voltage.
    raw_measured_voltage = ul.a_in(daq_device.board_num, channel, daq_device.get_ai_info().supported_ranges[0])
    measured_voltage = ul.to_eng_units(daq_device.board_num,
                                       daq_device.get_ai_info().supported_ranges[0],
                                       raw_measured_voltage)  # Convert to engineering units.
    return measured_voltage
