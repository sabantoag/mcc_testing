# mcc_testing

## Overview
This repository contains tools and scripts for testing and validating MCC (Modular Control Components) on Windows development environments. Requires InstaCal installed to identify the MCC DAQ plugged in. Board number setup on InstaCal currently has to be configured to be 0.

## Features
- Automated test scripts
- Sample configurations
- Logging and reporting utilities

## Getting Started

### Prerequisites
- Windows 10 or later
- Python 3.13+
- Git
- [InstaCal 6.7+](https://digilent.com/reference/software/start)

### Installation
1. Clone the repository:
    ```sh
    git clone https://github.com/yourusername/mcc_testing.git
    cd mcc_testing
    ```
2. Install dependencies:
    ```sh
    pip install -r requirements.txt
    ```

### Usage
Execute the pytest suite for a package:
```
pytest tests/<PACKAGE> --serial-number=<SERIAL_NUMBER> --part-number=<PART_NUMBER>
```
Example
```
pytest tests/9999-DD-2004 --serial-number=0123456789 --part-number=9999-DD-2004
```
To enable logging, add the --log-cli-level argument.
```
pytest tests/<PACKAGE> --serial-number=<SERIAL_NUMBER> --part-number=<PART_NUMBER> --log-cli-level=DEBUG
```

## Contributing
Contributions are welcome! Please open issues or submit pull requests.

## License
All Rights Reserved by Sabanto, Inc.
