#                                        --System Monitoring Application--

## Overview
This Python application provides a comprehensive system monitoring solution with features for real-time monitoring, 
alarm configuration, and a graphical user interface. 
It's designed to help users keep track of system resources and receive notifications for critical events.
It can be used not only separately but also it can be integrate with AWS CloudWatch, AWS QickSight, Grafana and Prometheus after making critical arrangment.

## Features
- Real-time system monitoring

- Configurable alarms for various system metrics. It can be entegrated any tool such as AWS CloudWatch, AWS QickSight, Grafana and so on.

- Email notifications for critical events.
    ### IMPORTANT : 
        For securely storing credentials, you should use one of the following services:
        1.HashiCorp Vault, 2.AWS Secrets Manager, 3.Azure Key Vault. 
        Dont write the credantials in the code (email_notifier.py), which deploys to git.

- Graphical User Interface (GUI) for easy interaction.

- Logging functionality for tracking application events.
    If you want you can arrange the file where the logs store. You can use: 
    "os.chdir("The path of the directory you want to store.")

## Prerequisites
- Python 3.12
- Required Python packages (install via `pip install -r requirements.txt`):
  - sendgrid (for email notifications)
  - psutil (for monitoring the system)
  

## Setup
1.  The repository: 
    https://github.com/ChasAcademy-HasanBalkanci/Project/tree/main/SystemDevelopmetPython


## The application will present a menu with the following options:
1. Start Monitoring
2. List Active Monitoring
3. Configure Alarms
4. Show Alarms
5. Remove Alarms
6. Start Monitoring Mode
7. Run GUI
8. Exit

## Components
- `main.py`: The main entry point of the application
- `menu.py`: Handles the display and interaction with the text-based menu
- `monitor.py`: Contains the `Monitor` class for system monitoring functionality
- `alarms.py`: Manages the `AlarmManager` for configuring and handling alarms
- `logger.py`: Provides logging functionality for the application
- `gui.py`: Implements the `MonitoringGUI` class for the graphical user interface

## Contributing
Contributions to this project are welcome. Please fork the repository and submit a pull request with your changes.


## Contact
Hasan Balkanci
hasan.balkanci@chasacademy.se


2. Install required packages:
    pip install -r requirements.txt

