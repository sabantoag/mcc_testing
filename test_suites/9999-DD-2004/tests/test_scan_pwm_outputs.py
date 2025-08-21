import logging
from time import sleep

from mcculw.device_info import DaqDeviceInfo
from mcculw import ul

from .daq_setup import setup_daq_device
from utils.polynomial import create_polynomial
from utils.daq_interface import measure_voltage
from utils.db_logger import log_test_result

logger = logging.getLogger(__name__)

# --- Hardware Configuration ---
FREQUENCY_HZ = 1000.0  # Frequency in Hz
TMR_CHANNEL_NUMBER = 0  # TMR pin on USB-1608G
ANALOG_INPUT_CHANNEL = 0  # Analog input channel for reading voltage
DIGITAL_OUT_LOW = 0  # Digital output low (auto) state

# --- Runtime Configuration ---
VOLTAGE_TOLERANCE_V = 0.15  # Tolerance for voltage measurement as a percentage of expected value
TIME_DELAY_S = 1.5  # Time delay in seconds to allow hardware state to update
# Calibrated coefficients for the polynomial used to compare against measured voltages.
# These coefficients should be derived from a known good calibration.
CALIBRATED_COEFFICIENTS = [-2.32407106, 6.482115, -8.96025862, 5.01013776]  # x^n + x^(n-1) + ... + x^0


def test_scan_pwm_outputs(daq_device: DaqDeviceInfo):
    try:
        digital_port, digital_pin = setup_daq_device(daq_device)
        ul.d_bit_out(daq_device.board_num, digital_port.type, digital_pin, DIGITAL_OUT_LOW)
        calibration_polynomial = create_polynomial(CALIBRATED_COEFFICIENTS)
        duty_cycles = [round(i * 0.05, 2) for i in range(1, 20)]

        for duty_cycle in duty_cycles:
            result = False
            measured_voltage = None
            expected_voltage = None
            actual_duty_cycle = duty_cycle  # Default fallback
            error_msg = None

            try:
                actual_frequency, actual_duty_cycle, _ = ul.pulse_out_start(
                    daq_device.board_num, TMR_CHANNEL_NUMBER, FREQUENCY_HZ, duty_cycle
                )
                actual_duty_cycle = round(actual_duty_cycle, 2)
                logger.debug(f'Outputting {actual_frequency} Hz with a duty cycle of {actual_duty_cycle} to '
                             f'channel {TMR_CHANNEL_NUMBER}')
                sleep(TIME_DELAY_S)
                measured_voltage = measure_voltage(daq_device, ANALOG_INPUT_CHANNEL)
                expected_voltage = calibration_polynomial(actual_duty_cycle)
                logger.debug(f'Measured voltage: {measured_voltage:.2f} V, Expected voltage: {expected_voltage:.2f} V')
                result = abs(measured_voltage - expected_voltage) <= VOLTAGE_TOLERANCE_V
                if not result:
                    error_msg = f'PWM output scan failed for duty cycle {duty_cycle}'
            except ul.ULError:
                error_msg = f'Duty cycle {duty_cycle} not supported by this device'
            except KeyboardInterrupt:
                error_msg = 'Test interrupted by user'
            except Exception as e:
                error_msg = f'Unexpected error: {e}'

            # Single logging call per duty cycle
            log_test_result(
                test_name=f'Scan PWM Output - Duty Cycle {actual_duty_cycle}',
                result_bool=result,
                measurement=measured_voltage,
                expected=expected_voltage
            )

            # Only assert if there was an error
            if error_msg:
                assert False, error_msg

    except Exception as e:
        assert False, f'Error during PWM output scan: {e}'
    finally:
        ul.pulse_out_stop(daq_device.board_num, TMR_CHANNEL_NUMBER)
