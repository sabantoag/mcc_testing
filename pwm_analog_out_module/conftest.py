import pytest
from mcculw import ul
from mcculw.enums import CounterChannelType
from mcculw.device_info import DaqDeviceInfo

from utils.db_logger import initialize_db

@pytest.fixture(scope="session")
def daq_device():
    """Initialize MCCULW DAQ device for testing."""
    # TODO: Find a new way to get the board number dynamically.
    board_number = 0

    try:
        daq_device_info = DaqDeviceInfo(board_number)
        print(f"\nActive DAQ device: {daq_device_info.product_name} ({daq_device_info.unique_id})\n")

        # TODO: Change this to check for device type to ensure same hardware is being used.
        if not daq_device_info.supports_counters:
            raise Exception('This device does not support counter operations.')

        ctr_info = daq_device_info.get_ctr_info()

        # Find any channel that supports timer capabilities
        first_timer_channel = next(
            (channel for channel in ctr_info.chan_info if channel.type in [CounterChannelType.CTRPULSE]),
            None
        )

        if not first_timer_channel:
            raise Exception('Error: The DAQ device does not support timer capabilities')

        # Yield daq_device_info for use in tests
        yield daq_device_info

    finally:
        # Clean up (if needed)
        ul.release_daq_device(daq_device_info.board_num)
        print("DAQ device released")


@pytest.fixture(scope="session", autouse=True)
def setup_database():
    initialize_db()
    print("Database initialized")
