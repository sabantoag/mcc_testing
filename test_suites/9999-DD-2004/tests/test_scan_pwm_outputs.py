import logging
from time import sleep
from typing import Tuple

from mcculw.device_info import DaqDeviceInfo
from mcculw.device_info.dio_info import PortInfo
from mcculw.enums import CounterChannelType, DigitalIODirection
from mcculw import ul
from utils.polynomial import create_polynomial, CALIBRATED_COEFFICIENTS
from utils.daq_interface import measure_voltage
from utils.db_logger import log_test_result

logger = logging.getLogger(__name__)

DIGITAL_OUTPUT_CHANNEL = 0  # Digital output pin used to switch SSRs between auto/manual states.
FREQUENCY_HZ = 1000.0  # Frequency in Hz
TMR_CHANNEL_NUMBER = 0  # TMR pin on USB-1608G
ANALOG_INPUT_CHANNEL = 0  # Analog input channel for reading voltage
DIGITAL_OUT_LOW = 0  # Digital output low (auto) state
# TODO: This will probably need to be adjusted via testing.
TOLERANCE = 0.5  # Tolerance for voltage measurement
TIME_DELAY_S = 1.5  # Time delay in seconds to allow hardware state to update


def test_scan_pwm_outputs(daq_device: DaqDeviceInfo):
    try:
        # Setup DAQ device for TIMER output to generate PWM signals.
        digital_port, digital_pin = _setup_daq_device(daq_device)
        ul.d_bit_out(daq_device.board_num, digital_port.type, digital_pin, DIGITAL_OUT_LOW)

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

                logger.debug(f'Outputting {actual_frequency} Hz with a duty cycle of {actual_duty_cycle} to '
                             f'channel {TMR_CHANNEL_NUMBER}')

                # Electronic settling time.
                sleep(TIME_DELAY_S)

                # Enable with analog input reading capabilities present.
                measured_voltage = measure_voltage(daq_device, ANALOG_INPUT_CHANNEL)
                # Grab theoretical voltage from polynomial.
                expected_voltage = calibration_polynomial(actual_duty_cycle)

                logger.debug(f'Measured voltage: {measured_voltage:.2f} V, Expected voltage: {expected_voltage:.2f} V')

                # # Check if measured voltage falls outside of expected calibrated value.
                result = True if abs(measured_voltage - expected_voltage) <= TOLERANCE else False

                log_test_result(
                    test_name=f'Scan PWM Output - Duty Cycle {duty_cycle}',
                    result_bool=result,
                    measurement=measured_voltage
                )
                # Assert statement to ensure when tests fail, we stop testing immediately.
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


def _setup_daq_device(daq_device: DaqDeviceInfo) -> Tuple[PortInfo, int]:
    def _setup_daq_device_digital(daq_device: DaqDeviceInfo) -> None:
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
        logger.debug(f'Setting {port.type.name} to {port_value}')

        # Output the values to configure the port.
        ul.d_out(daq_device.board_num, port.type, port_value)

        # Always using the first digital output pin.
        return port, DIGITAL_OUTPUT_CHANNEL

    def _setup_daq_device_timer(daq_device: DaqDeviceInfo) -> None:
        """
        Setup function to configure the DAQ device for TIMER output.
        This is a placeholder for any additional setup that may be required.
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
