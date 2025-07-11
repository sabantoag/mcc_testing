import logging
import pytest
from mcculw import ul
from mcculw.device_info import DaqDeviceInfo

from utils.db_logger import initialize_db

logger = logging.getLogger(__name__)


@pytest.fixture(scope="session")
def daq_device():
    """Initialize MCCULW DAQ device for testing."""
    # TODO: Find a new way to get the board number dynamically.
    # InstaCal currently sets this up as external tool.
    board_number = 0

    try:
        daq_device_info = DaqDeviceInfo(board_number)
        logger.debug(f"\nActive DAQ device: {daq_device_info.product_name} ({daq_device_info.unique_id})\n")

        # Yield daq_device_info for use in tests
        yield daq_device_info
    finally:
        # Clean up (if needed)
        ul.release_daq_device(daq_device_info.board_num)
        logger.debug("DAQ device released")


@pytest.fixture(scope="session", autouse=True)
def setup_database():
    initialize_db()
    logger.debug("Database initialized")
