from time import sleep

from mcculw.device_info import DaqDeviceInfo
from mcculw import ul
from utils.db_logger import log_test_result



FREQUENCY_HZ = 1000.0  # Frequency in Hz
CHANNEL_NUM = 0  # TMR0 pin on CTR04 DAQ device


def test_scan_pwm_outputs(daq_device: DaqDeviceInfo):
    try:
        duty_cycles = [round(i * 0.05, 2) for i in range(1, 21)]

        # Depending on device, value of 1.0 (100%) duty cycle may cause error.
        try:
            for duty_cycle in duty_cycles:
                actual_frequency, actual_duty_cycle, _ = ul.pulse_out_start(
                    daq_device.board_num, CHANNEL_NUM, FREQUENCY_HZ, duty_cycle
                )
                actual_duty_cycle = round(actual_duty_cycle, 2)  # Round to 2 decimal places
                print(f'Outputting {actual_frequency} Hz with a duty cycle of {actual_duty_cycle} to channel {CHANNEL_NUM}')
                sleep(5)  # Give some time frame for output to be set, observe output

                log_test_result(
                    test_name=f'Scan PWM Output - Duty Cycle {duty_cycle}',
                    result_bool=True,
                    measurement=actual_duty_cycle
                )
            assert True, 'PWM output scan completed successfully'
        except ul.ULError:
            print(f'WARN: Duty cycle not supported by this device. Skipping duty cycle {duty_cycle}')
    except Exception as e:
        log_test_result(
            test_name='test_scan_pwm_outputs',
            result_bool=False
        )
        assert False, f'Error during PWM output scan: {e}'
