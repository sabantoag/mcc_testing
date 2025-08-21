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
- Python 3.8+
- Git
- [InstaCal 6.7+](https://digilent.com/reference/software/start)
- [Inno Setup 6.5.1+](https://jrsoftware.org/isinfo.php)
- [VC++](https://aka.ms/vs/17/release/vc_redist.x64.exe)

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
pytest test_suites/
```
Or with html generation
```
pytest test_suites/ --html=reports/report.html --self-contained-html
```

## Contributing
Contributions are welcome! Please open issues or submit pull requests.

## License
All Rights Reserved by Sabanto, Inc.
