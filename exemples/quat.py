"""Example script to read quaternion data from BMI088 sensor."""

import time

from bmi088 import BMI088

imu = BMI088(i2c_bus=4)

while True:
    quat = imu.get_quat()
    print("Quaternion:", quat)

    time.sleep(0.1)
