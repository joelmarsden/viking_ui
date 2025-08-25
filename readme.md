# Overview

    This software supports the Viking project

    The software reads and displays sensor data from an embedded Raspberry Pi Zero W:
        - Temperature (MLX90614) - infra-read thermomenter
        - Heart Rate  (Pulse Sensor - https://pulsesensor.com) via ADC converter ads1x15
        - Gyroscope/Accelerometer  (MPU6050) - 3axis gyroscope and 3axis accelerometer

    Functionality:
        - user can view the sensor data
        - sensor data is updated once per second
        - user can set alerts against the sensors

    Notes:
        - the project was built using WiFi rather than bluetooth due to apple licensing restrictions on bluetooth

    Future Enhancements:
        - bluetooth support
        - push notifications alerts

# Setup - Raspberry PI

    sudo raspi-config
    Select Interfacing Options -> I2C

    sudo apt install python3-smbus

# Python - Package Requirements

## MPU6050

    https://www.instructables.com/How-to-Use-the-MPU6050-With-the-Raspberry-Pi-4/
    pip install mpu6050-raspberrypi

## PyMLX90614

    https://pypi.org/project/PyMLX90614/
    pip install PyMLX90614-0.0.4-py3-none-any.whl

## ADC (Analog to Digital Converter)

    pip install adafruit-ads1x15

## Flask (webserver)

    https://pypi.org/project/Flask/
    pip install Flask

# Circuit Diagram

    Refer to folio for wiring diagrams

# Check I2C Devices are connected correctly after wiring

    sudo i2cdetect -y 1
    
         0  1  2  3  4  5  6  7  8  9  a  b  c  d  e  f
    00:          -- -- -- -- -- -- -- -- -- -- -- -- -- 
    10: -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- 
    20: -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- 
    30: -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- 
    40: -- -- -- -- -- -- -- -- 48 -- -- -- -- -- -- -- 
    50: -- -- -- -- -- -- -- -- -- -- 5a -- -- -- -- -- 
    60: -- -- -- -- -- -- -- -- 68 -- -- -- -- -- -- -- 
    70: -- -- -- -- -- -- -- --      



