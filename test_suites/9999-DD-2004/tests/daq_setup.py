import logging
from typing import Tuple

from mcculw.device_info import DaqDeviceInfo
from mcculw.device_info.dio_info import PortInfo
from mcculw.enums import CounterChannelType, DigitalIODirection
from mcculw import ul


logger = logging.getLogger(__name__)

# --- Hardware Configuration ---
DIGITAL_OUTPUT_CHANNEL = 0  # Digital output pin used to switch SSRs between auto/manual states.


def setup_daq_device(daq_device: DaqDeviceInfo) -> Tuple[PortInfo, int]:
    """Setup MCC DAQ device timer and digital outs for testing.

    Args:
        daq_device (DaqDeviceInfo): MCC DAQ device information provided by the MCCULW library.

    Raises:
        Exception: If DAQ device doesn't support the required digital I/O or timer operations.

    Returns:
        Tuple[PortInfo, int]: Digital out PortInfo with corresponding pin number.
    """
    def _setup_daq_device_digital(daq_device: DaqDeviceInfo) -> Tuple[PortInfo, int]:
        """Setup MCC DAQ device for digital output.

        Args:
            daq_device (DaqDeviceInfo): MCC DAQ device information provided by the MCCULW library.

        Raises:
            Exception: DAQ device does not support digital I/O.
            Exception: DAQ device pins do not support digital output.
            Exception: DAQ device port is not configured for output.
            Exception: DAQ device digital pins do not support configuration as output.

        Returns:
            Tuple[PortInfo, int]: PortInfo of the digital output port and corresponding pin number.
        """
        if not daq_device.supports_digital_io:
            raise Exception('Error: The DAQ device does not support '
                            'digital I/O')

        dio_info = daq_device.get_dio_info()

        # TODO: Make this configurable or pass as an argument for the digital pin of interest.
        # Find the first port that supports input, defaulting to None
        # if one is not found.
        port = next((port for port in dio_info.port_info if port.supports_output),
                    None)
        if not port:
            raise Exception('Error: The DAQ device does not support '
                            'digital output')

        # If the port is configurable, configure it for output.
        if port.is_port_configurable:
            ul.d_config_port(daq_device.board_num, port.type, DigitalIODirection.OUT)
        elif port.type != DigitalIODirection.OUT:
            raise Exception('Error: The port is not configured for output')
        else:
            raise Exception('Error: The port is not configurable for output')

        port_value = 0xFF
        logger.debug(f'Setting {port.type.name} to {port_value}')

        # Output the values to configure the port.
        ul.d_out(daq_device.board_num, port.type, port_value)

        # Always using the first digital output pin.
        return port, DIGITAL_OUTPUT_CHANNEL

    def _setup_daq_device_timer(daq_device: DaqDeviceInfo) -> None:
        """Setup function to configure the DAQ device for TIMER output.

        Args:
            daq_device (DaqDeviceInfo): MCC DAQ device information provided by the MCCULW library.

        Raises:
            Exception: DAQ Device or TMR pin does not support counter operations.
        """
        if not daq_device.supports_counters:
            raise Exception('This device does not support counter operations.')

        ctr_info = daq_device.get_ctr_info()

        # Find any channel that supports timer capabilities
        first_timer_channel = next(
            (channel for channel in ctr_info.chan_info if channel.type in [CounterChannelType.CTRPULSE]),
            None
        )

        if not first_timer_channel:
            raise Exception('Error: The DAQ device does not support timer capabilities')

    # Configure the DAQ device for digital output and timer output.
    digital_port, digital_out_pin = _setup_daq_device_digital(daq_device)
    _setup_daq_device_timer(daq_device)

    return digital_port, digital_out_pin
