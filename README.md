# Veyon Master Counteraction Program

## Overview
This program is designed to detect and manage connections made by the Veyon Master application. It provides a simple interface to monitor connection status and manage the Veyon Master service.

## Installation and Usage

### Requirements
- Python 3.x installed on your system (if running the script).
- Required libraries specified in the `requirements.txt`.

### Setup Options
1. **Run the Script**:
   - Install the required libraries by running:
     ```bash
     pip install -r requirements.txt
     ```
   - Execute the script:
     ```bash
     python main.py
     ```

2. **Use Precompiled EXE**:
   - Run the provided `.exe` file directly, no additional setup required.

### How It Works
1. On launch, the program checks if **Veyon Master** is installed on your PC:
   - If **not installed**, the program will terminate.
   - If **installed**, a red square icon will appear in the system tray.

2. Right-clicking the red square opens a menu with the following options:
   - **Status**: View the current status of Veyon Master.
   - **Disable/Restart Veyon Master**: Allows disabling or restarting the Veyon Master service (only if the program is run with administrator privileges and the service is running).
   - **Exit**: Close the program.



## Disclaimer
Administrator privileges are required for some functionality. Ensure you have the appropriate permissions before use.
