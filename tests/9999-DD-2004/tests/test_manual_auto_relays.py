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
DIGITAL_OUT_AUTO = 0
DIGITAL_OUT_MANUAL = 1

# --- Runtime Configuration ---
# Time delay in seconds to allow hardware state to update
TIME_DELAY_S = 1
# Voltage divider circuit from 5V to 2.5V (R1=1k, R2=2.2k) with ~1.56mA current draw.
# This is the expected voltage when the SSR is in manual mode to simulate external
# circuitry that would be from the tractor.
EXPECTED_MANUAL_INPUT_VOLTAGE = 3.5
# TMR pin should be set to 0 duty cycle, so the voltage should be close to supply voltage (+5V) for auto mode.
EXPECTED_AUTO_VOLTAGE = 4.75
MINIMUM_VOLTAGE = 2.75  # Minimum voltage to consider as a valid HIGH signal (half of 5V supply)


def test_auto_mode(daq_device: DaqDeviceInfo):
    result = False
    measured_voltage = None
    error_msg = None

    try:
        # Setup the first digital output pin on the DAQ device for digital out functionality.
        # Digital output pin should be set with a pull down resistor to pull to ground when set high. This is done
        # via opening the DAQ device and adjusting the jumper on the board.
        port, digital_out_pin = setup_daq_device(daq_device)  # Setup the DAQ device for digital output.
        ul.d_bit_out(daq_device.board_num, port.type, digital_out_pin, DIGITAL_OUT_AUTO)

        # Flip digital pin to manual mode.

        sleep(TIME_DELAY_S)  # Allow time for the state to change
        measured_voltage = measure_voltage(daq_device, ANALOG_INPUT)

        # Get result of test by comparing measured voltage to expected voltage from +5V power supply passed into
        # analog input channel.
        logger.debug(f'Measured voltage in auto mode: {measured_voltage:.2f} V')
        result = measured_voltage >= EXPECTED_AUTO_VOLTAGE

        if not result:
            error_msg = f"Auto mode test result as {result} with measured voltage: {measured_voltage:.2f} V"
    except Exception as e:
        logger.debug(f"An error occurred during auto mode test: {e}")
        error_msg = f"Auto mode test failed with error: {e}"
    finally:
        # Open circuit to switch hardware back to auto state.
        port, digital_out_pin = setup_daq_device(daq_device)  # Setup the DAQ device for digital output.
        ul.d_bit_out(daq_device.board_num, port.type, digital_out_pin, DIGITAL_OUT_MANUAL)

    # Log test results with assertion to ensure test failure is captured in db and test suite exits.
    log_test_result(
        test_name="Auto Mode Test",
        result_bool=result,
        measurement=measured_voltage,
        expected=EXPECTED_AUTO_VOLTAGE
    )
    assert result, error_msg


def test_manual_mode(daq_device: DaqDeviceInfo):
    result = False
    measured_voltage = None
    error_msg = None

    try:
        # Setup the first digital output pin on the DAQ device for digital out functionality.
        # Digital output pin should be set with a pull down resistor to pull to ground when set high. This is done
        # via opening the DAQ device and adjusting the jumper on the board.
        port, digital_out_pin = setup_daq_device(daq_device)  # Setup the DAQ device for digital output.
        ul.d_bit_out(daq_device.board_num, port.type, digital_out_pin, DIGITAL_OUT_MANUAL)

        # Flip digital pin to manual mode.

        sleep(TIME_DELAY_S)  # Allow time for the state to change
        measured_voltage = measure_voltage(daq_device, ANALOG_INPUT)

        # Get result of test by comparing measured voltage to expected voltage from +5V power supply passed into
        # analog input channel.
        logger.debug(f'Measured voltage in manual mode: {measured_voltage:.2f} V')
        result = MINIMUM_VOLTAGE <= measured_voltage <= EXPECTED_MANUAL_INPUT_VOLTAGE

        if not result:
            error_msg = f"Manual mode test result as {result} with measured voltage: {measured_voltage:.2f} V"
    except Exception as e:
        logger.debug(f"An error occurred during manual mode test: {e}")
        error_msg = f"Manual mode test failed with error: {e}"
    finally:
        # Open circuit to switch hardware back to auto state.
        port, digital_out_pin = setup_daq_device(daq_device)  # Setup the DAQ device for digital output.
        ul.d_bit_out(daq_device.board_num, port.type, digital_out_pin, DIGITAL_OUT_MANUAL)

    # Log test results with assertion to ensure test failure is captured in db and test suite exits.
    log_test_result(
        test_name="Manual Mode Test",
        result_bool=result,
        measurement=measured_voltage,
        expected=EXPECTED_MANUAL_INPUT_VOLTAGE
    )
    assert result, error_msg
