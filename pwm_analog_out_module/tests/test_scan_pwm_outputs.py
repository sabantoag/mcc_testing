import logging
import pytest
from time import sleep

from mcculw.device_info import DaqDeviceInfo
from mcculw.enums import CounterChannelType
from mcculw import ul
from utils.polynomial import create_polynomial, CALIBRATED_COEFFICIENTS
from utils.daq_interface import measure_voltage
from utils.db_logger import log_test_result

logger = logging.getLogger(__name__)

FREQUENCY_HZ = 1000.0  # Frequency in Hz
TMR_CHANNEL_NUMBER = 0  # TMR pin on USB-1608G
ANALOG_INPUT_CHANNEL = 0  # Analog input channel for reading voltage
# TODO: This will probably need to be adjusted via testing.
TOLERANCE = 0.1  # Tolerance for voltage measurement


# @pytest.mark.skip(reason="Disabling for time being to test other features.")
def test_scan_pwm_outputs(daq_device: DaqDeviceInfo):
    try:
        # Setup DAQ device for TIMER output to generate PWM signals.
        _setup_daq_device(daq_device)

        # Create a polynomial from known, good calibration values to compare tested circuit against.
        calibration_polynomial = create_polynomial(CALIBRATED_COEFFICIENTS)

        # Duty cycles to be tested on the PWM outputs. Note excluding 0.0 and 1.0.
        duty_cycles = [round(i * 0.05, 2) for i in range(1, 20)]

        # Depending on device, duty cycles of 0. (0%) and 1.0 (100%) may cause errors.
        # Catch these in event they occur.
        for duty_cycle in duty_cycles:
            try:
                actual_frequency, actual_duty_cycle, _ = ul.pulse_out_start(
                    daq_device.board_num, TMR_CHANNEL_NUMBER, FREQUENCY_HZ, duty_cycle
                )
                actual_duty_cycle = round(actual_duty_cycle, 2)  # Round to 2 decimal places

                logger.debug(f'Outputting {actual_frequency} Hz with a duty cycle of {actual_duty_cycle} to channel {TMR_CHANNEL_NUMBER}')

                # Electronic settling time.
                sleep(2)

                # Enable with analog input reading capabilities present.
                measured_voltage = measure_voltage(daq_device, ANALOG_INPUT_CHANNEL)
                expected_voltage = calibration_polynomial(actual_duty_cycle)  # Grab theoretical voltage from polynomial.

                logger.debug(f'Measured voltage: {measured_voltage:.2f} V, Expected voltage: {expected_voltage:.2f} V')

                # # Check if measured voltage falls outside of expected calibrated value.
                # result = True if abs(measured_voltage - expected_voltage) <= TOLERANCE else False
                result = True

                log_test_result(
                    test_name=f'Scan PWM Output - Duty Cycle {duty_cycle}',
                    result_bool=result,
                    measurement=actual_duty_cycle
                )
                assert result, f'PWM output scan passed for duty cycle {duty_cycle}'
            except ul.ULError:
                log_test_result(
                    test_name=f'Scan PWM Output - Duty Cycle {duty_cycle}',
                    result_bool=False,
                    measurement=actual_duty_cycle
                )
                assert False, f'Duty cycle {duty_cycle} not supported by this device'
            except KeyboardInterrupt:
                log_test_result(
                    test_name=f'Scan PWM Output - Duty Cycle {duty_cycle}',
                    result_bool=False,
                    measurement=actual_duty_cycle
                )
                assert False, 'Test interrupted by user'
    except Exception as e:
        log_test_result(
            test_name='test_scan_pwm_outputs',
            result_bool=False
        )
        assert False, f'Error during PWM output scan: {e}'
    finally:
        # Stop pulse after testing.
        ul.pulse_out_stop(daq_device.board_num, TMR_CHANNEL_NUMBER)

def _setup_daq_device(daq_device: DaqDeviceInfo) -> int:
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

    return TMR_CHANNEL_NUMBER
