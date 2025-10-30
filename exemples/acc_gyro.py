"""Example script to read acceleration and gyroscope data from BMI088 sensor."""

import time

from bmi088 import BMI088

imu = BMI088(i2c_bus=4)

while True:
    acceleration = imu.read_accelerometer()
    print(
        f"Acceleration: X={acceleration[0]}, Y={acceleration[1]}, Z={acceleration[2]}"
    )

    gyroscope = imu.read_gyroscope()
    print(f"Gyroscope: X={gyroscope[0]}, Y={gyroscope[1]}, Z={gyroscope[2]}")
    time.sleep(0.1)
