import logging
from time import sleep

from mcculw.device_info import DaqDeviceInfo
from mcculw import ul

from .daq_setup import setup_daq_device
from utils.polynomial import create_polynomial, CALIBRATED_COEFFICIENTS
from utils.daq_interface import measure_voltage
from utils.db_logger import log_test_result

logger = logging.getLogger(__name__)

# --- Hardware Configuration ---
FREQUENCY_HZ = 1000.0  # Frequency in Hz
TMR_CHANNEL_NUMBER = 0  # TMR pin on USB-1608G
ANALOG_INPUT_CHANNEL = 0  # Analog input channel for reading voltage
DIGITAL_OUT_LOW = 0  # Digital output low (auto) state

# --- Runtime Configuration ---
# TODO: This will probably need to be adjusted via testing.
VOLTAGE_TOLERANCE = 0.5  # Tolerance for voltage measurement
TIME_DELAY_S = 1.5  # Time delay in seconds to allow hardware state to update


def test_scan_pwm_outputs(daq_device: DaqDeviceInfo):
    try:
        # Setup DAQ device for TIMER output to generate PWM signals.
        digital_port, digital_pin = setup_daq_device(daq_device)
        ul.d_bit_out(daq_device.board_num, digital_port.type, digital_pin, DIGITAL_OUT_LOW)

        # Create a polynomial from known, good calibration values to compare tested circuit against.
        calibration_polynomial = create_polynomial(CALIBRATED_COEFFICIENTS)

        # Duty cycles to be tested on the PWM outputs. Note excluding 0.0 and 1.0.
        duty_cycles = [round(i * 0.05, 2) for i in range(1, 20)]

        # Depending on device, duty cycles of 0. (0%) and 1.0 (100%) may cause errors.
        # Catch these in event they occur.
        for duty_cycle in duty_cycles:
            result = False
            measured_voltage = None
            error_msg = None
            actual_duty_cycle = duty_cycle  # Default fallback

            try:
                actual_frequency, actual_duty_cycle, _ = ul.pulse_out_start(
                    daq_device.board_num, TMR_CHANNEL_NUMBER, FREQUENCY_HZ, duty_cycle
                )
                actual_duty_cycle = round(actual_duty_cycle, 2)  # Round to 2 decimal places

                logger.debug(f'Outputting {actual_frequency} Hz with a duty cycle of {actual_duty_cycle} to '
                             f'channel {TMR_CHANNEL_NUMBER}')

                # Electronic settling time.
                sleep(TIME_DELAY_S)

                # Enable with analog input reading capabilities present.
                measured_voltage = measure_voltage(daq_device, ANALOG_INPUT_CHANNEL)
                # Grab theoretical voltage from polynomial.
                expected_voltage = calibration_polynomial(actual_duty_cycle)

                logger.debug(f'Measured voltage: {measured_voltage:.2f} V, Expected voltage: {expected_voltage:.2f} V')

                # Check if measured voltage falls outside of expected calibrated value.
                result = abs(measured_voltage - expected_voltage) <= VOLTAGE_TOLERANCE

                if not result:
                    error_msg = f'PWM output scan failed for duty cycle {duty_cycle}'

            except ul.ULError:
                error_msg = f'Duty cycle {duty_cycle} not supported by this device'
                measured_voltage = None
                # Assert false to ensure test failure is captured in db and test suite exits.
                assert False, error_msg
            except KeyboardInterrupt:
                error_msg = 'Test interrupted by user'
                measured_voltage = None
                # Assert false to ensure test failure is captured in db and test suite exits.
                assert result, error_msg

            # Single logging call for each duty cycle test
            log_test_result(
                test_name=f'Scan PWM Output - Duty Cycle {actual_duty_cycle}',
                result_bool=result,
                measurement=measured_voltage
            )
    except Exception as e:
        # Log here to db to capture internal exception raised during the test execution.
        log_test_result(
            test_name='test_scan_pwm_outputs',
            result_bool=False,
            measurement=None
        )
        assert False, f'Error during PWM output scan: {e}'
    finally:
        # Stop pulse after testing.
        ul.pulse_out_stop(daq_device.board_num, TMR_CHANNEL_NUMBER)
