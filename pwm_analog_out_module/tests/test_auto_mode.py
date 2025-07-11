import logging
from time import sleep
from typing import Tuple

from mcculw.device_info import DaqDeviceInfo
from mcculw.device_info.dio_info import PortInfo
from mcculw.enums import DigitalIODirection
from mcculw import ul
from utils.daq_interface import measure_voltage
from utils.db_logger import log_test_result

logger = logging.getLogger(__name__)

DIGITAL_OUTPUT_CHANNEL = 0  # Digital output pin used to switch SSRs between auto/manual states.
AUTO_ANALOG_INPUT_CHANNEL = 9  # Analog input channel used to read manual mode voltage.
EXPECTED_INPUT_VOLTAGE = 4.75  # Expected voltage in manual mode as test stand passes +5V into analog input channel.
DIGITAL_OUT_LOW = 0
DIGITAL_OUT_HIGH = 1
TIME_DELAY_S = 2  # Time delay in seconds to allow hardware state to update


def test_auto_mode(daq_device: DaqDeviceInfo):
    try:
        # Setup the first digital output pin on the DAQ device for digital out functionality.
        # Digital output pin should be set with a pull down resistor to pull to ground when set high. This is done
        # via opening the DAQ device and adjusting the jumper on the board.
        port, digital_out_pin = _setup_daq_device(daq_device)  # Setup the DAQ device for digital output.
        ul.d_bit_out(daq_device.board_num, port.type, digital_out_pin, DIGITAL_OUT_LOW)

        # Flip digital pin to manual mode.

        sleep(TIME_DELAY_S)  # Allow time for the state to change
        measured_voltage = measure_voltage(daq_device, AUTO_ANALOG_INPUT_CHANNEL)

        # Get result of test by comparing measured voltage to expected voltage from +5V power supply passed into analog input channel.
        logger.debug(f'Measured voltage in auto mode: {measured_voltage:.2f} V')
        result = True if measured_voltage >= EXPECTED_INPUT_VOLTAGE else False

        log_test_result(
            test_name="Auto Mode Test",
            result_bool=result,
            measurement=measured_voltage
        )
        assert result, f"Auto mode test result as {result} with measured voltage: {measured_voltage:.2f} V"
    except Exception as e:
        logger.debug(f"An error occurred during auto mode test: {e}")
        log_test_result(
            test_name="Auto Mode Test",
            result_bool=False,
            measurement=None,
        )
        assert False, f"Auto mode test failed with error: {e}"


def _setup_daq_device(daq_device: DaqDeviceInfo) -> Tuple[PortInfo, int]:
    """
    Setup function to configure the DAQ device for PWM output.
    This is a placeholder for any additional setup that may be required.
    """
    if not daq_device.supports_digital_io:
        raise Exception('Error: The DAQ device does not support '
                        'digital I/O')

    dio_info = daq_device.get_dio_info()

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

    port_value = 0xFF
    logger.debug('Setting', port.type.name, 'to', port_value)

    # Output the values to configure the port.
    ul.d_out(daq_device.board_num, port.type, port_value)

    # Always using the first digital output pin.
    return port, DIGITAL_OUTPUT_CHANNEL
