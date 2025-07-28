import logging
from time import sleep

from mcculw.device_info import DaqDeviceInfo
from mcculw import ul

from .daq_setup import setup_daq_device
from utils.daq_interface import measure_voltage
from utils.db_logger import log_test_result

logger = logging.getLogger(__name__)

# --- Hardware Configuration ---
DIGITAL_OUTPUT_CHANNEL = 0  # Digital output pin used to switch SSRs between auto/manual states.
ANALOG_INPUT = 0  # Analog input channel used to read manual mode voltage.
DIGITAL_OUT_LOW = 0
DIGITAL_OUT_HIGH = 1

# --- Runtime Configuration ---
TIME_DELAY_S = 1  # Time delay in seconds to allow hardware state to update
EXPECTED_INPUT_VOLTAGE = 4.75  # Expected voltage in manual mode as test stand passes +5V into analog input channel.


def test_auto_mode(daq_device: DaqDeviceInfo):
    try:
        # Setup the first digital output pin on the DAQ device for digital out functionality.
        # Digital output pin should be set with a pull down resistor to pull to ground when set high. This is done
        # via opening the DAQ device and adjusting the jumper on the board.
        port, digital_out_pin = setup_daq_device(daq_device)  # Setup the DAQ device for digital output.
        ul.d_bit_out(daq_device.board_num, port.type, digital_out_pin, DIGITAL_OUT_LOW)

        # Flip digital pin to manual mode.

        sleep(TIME_DELAY_S)  # Allow time for the state to change
        measured_voltage = measure_voltage(daq_device, ANALOG_INPUT)

        # Get result of test by comparing measured voltage to expected voltage from +5V power supply passed into
        # analog input channel.
        logger.debug(f'Measured voltage in auto mode: {measured_voltage:.2f} V')
        result = True if measured_voltage <= EXPECTED_INPUT_VOLTAGE else False

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


def test_manual_mode(daq_device: DaqDeviceInfo):
    try:
        # Setup the first digital output pin on the DAQ device for digital out functionality.
        # Digital output pin should be set with a pull down resistor to pull to ground when set high. This is done
        # via opening the DAQ device and adjusting the jumper on the board.
        port, digital_out_pin = setup_daq_device(daq_device)  # Setup the DAQ device for digital output.
        ul.d_bit_out(daq_device.board_num, port.type, digital_out_pin, DIGITAL_OUT_HIGH)

        # Flip digital pin to manual mode.

        sleep(TIME_DELAY_S)  # Allow time for the state to change
        measured_voltage = measure_voltage(daq_device, ANALOG_INPUT)

        # Get result of test by comparing measured voltage to expected voltage from +5V power supply passed into
        # analog input channel.
        logger.debug(f'Measured voltage in manual mode: {measured_voltage:.2f} V')
        result = True if measured_voltage >= EXPECTED_INPUT_VOLTAGE else False

        log_test_result(
            test_name="Manual Mode Test",
            result_bool=result,
            measurement=measured_voltage
        )
        assert result, f"Manual mode test result as {result} with measured voltage: {measured_voltage:.2f} V"
    except Exception as e:
        print(f"An error occurred during manual mode test: {e}")
        log_test_result(
            test_name="Manual Mode Test",
            result_bool=False,
            measurement=None,
        )
        assert False, f"Manual mode test failed with error: {e}"
