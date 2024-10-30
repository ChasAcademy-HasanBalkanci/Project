# System Monitoring Application

## Overview

This System Monitoring Application is a Python-based tool that allows users to monitor CPU, memory, and disk usage on their system. It provides features such as real-time monitoring, configurable alarms, logging, and a simple graphical interface.

## Features

- Real-time monitoring of CPU, memory, and disk usage
- Configurable alarms for different usage thresholds
- Logging of all events and user interactions
- Persistence of alarm configurations
- Email notifications for triggered alarms
- Simple graphical interface for live monitoring
- Console-based menu for easy interaction

## Requirements

- Python 3.7+
- psutil
- sendgrid

## Installation

1. Clone the repository:
git clone https://github.com/yourusername/system-monitoring-app.git
cd system-monitoring-app


2. Install the required packages:
pip install psutil sendgrid


3. Configure the SendGrid API key and email addresses in `config.py`:
```python
SENDGRID_API_KEY = 'your_sendgrid_api_key'
EMAIL_FROM = 'your_email@example.com'
EMAIL_TO = 'recipient@example.com'

** Usage **

Run the application by executing:
python main.py

The main menu will provide the following options:

Start monitoring

List active monitoring

Create alarms

Show alarms

Start monitoring mode

Remove alarms

Start GUI

Exit

Follow the on-screen prompts to interact with the application.

File Structure
main.py: Entry point of the application

monitoring_app.py: Main application class

system_monitor.py: Class for system monitoring

alarm_manager.py: Class for managing alarms

logger.py: Class for logging

utils.py: Utility functions

gui.py: Simple graphical interface

config.py: Configuration settings

Logging
Logs are stored in the logs directory. Each log file is named with the timestamp of when the application was started.

Alarm Configuration
Alarms are stored in alarms.json and are loaded each time the application starts.

GUI
The graphical interface displays real-time system usage and active alarms. To start the GUI, select option 7 from the main menu.

Contributing
Contributions are welcome! Please feel free to submit a Pull Request.
