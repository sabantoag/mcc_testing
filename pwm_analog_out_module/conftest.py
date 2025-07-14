import logging
import pytest
import pytest_html
from mcculw import ul
from mcculw.device_info import DaqDeviceInfo

from utils.db_logger import initialize_db, fetch_test_results, clear_test_results

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
    clear_test_results()
    logger.debug("Database initialized")


def pytest_html_report_title(report):
    """Customize the HTML report title."""
    report.title = f"9999-DD-2004 Test Report"


def pytest_html_results_summary(prefix, summary, postfix):
    results = fetch_test_results()
    if results:
        html = ['<h2>Database Test Results</h2>',
                '<table border="1"><tr><th>Test Name</th><th>Result</th><th>Measurement</th><th>Timestamp</th></tr>']
        for test_name, result, measurement, timestamp in results:
            if result == "FAIL":
                row = f'<tr style="background-color: #ffe0e0;"><td>{test_name}</td><td>{result}</td><td>{measurement}</td><td>{timestamp}</td></tr>'
            else:
                row = f'<tr><td>{test_name}</td><td>{result}</td><td>{measurement}</td><td>{timestamp}</td></tr>'
            html.append(row)
        html.append('</table>')
        summary.extend([pytest_html.extras.html(''.join(html))])
