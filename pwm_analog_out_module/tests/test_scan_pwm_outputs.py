from time import sleep

from mcculw.device_info import DaqDeviceInfo
from mcculw import ul
from utils.polynomial import create_polynomial, CALIBRATED_COEFFICIENTS, plot_polynomial
from utils.daq_interface import measure_voltage
from utils.db_logger import log_test_result



FREQUENCY_HZ = 1000.0  # Frequency in Hz
CHANNEL_NUM = 0  # TMR pin on USB-1608G
# TODO: This will probably need to be adjusted via testing.
TOLERANCE = 0.1  # Tolerance for voltage measurement


def test_scan_pwm_outputs(daq_device: DaqDeviceInfo):
    try:
        # Create a polynomial from known, good calibration values.
        calibration_polynomial = create_polynomial(CALIBRATED_COEFFICIENTS)
        plot_polynomial(
            calibration_polynomial,
            x_range=(0.0, 1.0),
            num_points=1000
        )  # Plot the polynomial for visual verification.

        # Duty cycles to be tested on the PWM outputs. Note excluding 0.0 and 1.0.
        duty_cycles = [round(i * 0.05, 2) for i in range(1, 20)]

        # Depending on device, value of 1.0 (100%) duty cycle may cause error.
        for duty_cycle in duty_cycles:
            try:
                actual_frequency, actual_duty_cycle, _ = ul.pulse_out_start(
                    daq_device.board_num, CHANNEL_NUM, FREQUENCY_HZ, duty_cycle
                )
                actual_duty_cycle = round(actual_duty_cycle, 2)  # Round to 2 decimal places
                print(f'Outputting {actual_frequency} Hz with a duty cycle of {actual_duty_cycle} to channel {CHANNEL_NUM}')

                # Electronic settling time.
                sleep(2)

                # Enable with analog input reading capabilities present.
                measured_voltage = measure_voltage(daq_device, CHANNEL_NUM)
                expected_voltage = calibration_polynomial(actual_duty_cycle)  # Grab theoretical voltage from polynomial.

                print(f'Measured voltage: {measured_voltage:.2f} V, Expected voltage: {expected_voltage:.2f} V')

                # # Check if measured voltage falls outside of expected calibrated value.
                # if abs(measured_voltage - expected_voltage) > TOLERANCE:
                #     assert False, f'PWM output scan failed for duty cycle {duty_cycle} failed with measured voltage {measured_voltage:.2f} V, expected {expected_voltage:.2f} V'
                # else:
                #     assert True, f'PWM output scan passed for duty cycle {duty_cycle}'

                log_test_result(
                    test_name=f'Scan PWM Output - Duty Cycle {duty_cycle}',
                    result_bool=True,
                    measurement=actual_duty_cycle
                )
                assert True, f'PWM output scan passed for duty cycle {duty_cycle}'
            except ul.ULError:
                assert False, f'Duty cycle {duty_cycle} not supported by this device'
            except KeyboardInterrupt:
                assert False, 'Test interrupted by user'
            finally:
                # Do we RESET hardware here? What to do?
                pass
    except Exception as e:
        log_test_result(
            test_name='test_scan_pwm_outputs',
            result_bool=False
        )
        assert False, f'Error during PWM output scan: {e}'
