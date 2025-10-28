"""BMI088 sensor interface module."""

from enum import Enum

import numpy as np
from smbus3 import SMBus

ACC_ADDRESS = 0x18
GYRO_ADDRESS = 0x69

ACC_ENABLE_ADDRESS = 0x7D

ACC_ON = 0x04

ACC_X_LSB = 0x12
ACC_X_MSB = 0x13
ACC_Y_LSB = 0x14
ACC_Y_MSB = 0x15
ACC_Z_LSB = 0x16
ACC_Z_MSB = 0x17

GYRO_RATE_X_LSB = 0x02
GYRO_RATE_X_MSB = 0x03
GYRO_RATE_Y_LSB = 0x04
GYRO_RATE_Y_MSB = 0x05
GYRO_RATE_Z_LSB = 0x06
GYRO_RATE_Z_MSB = 0x07

TEMP_MSB = 0x22
TEMP_LSB = 0x23


class AccRange(Enum):
    """Accelerometer range settings."""

    RANGE_3G = 0
    RANGE_6G = 1
    RANGE_12G = 2
    RANGE_24G = 3


class AccBandwidth(Enum):
    """Accelerometer filter bandwidth settings."""

    BANDWIDTH_12_5 = 0xA5
    BANDWIDTH_25 = 0xA6
    BANDWIDTH_50 = 0xA7
    BANDWIDTH_100 = 0xA8
    BANDWIDTH_200 = 0xA9
    BANDWIDTH_400 = 0xAA
    BANDWIDTH_800 = 0xAB
    BANDWIDTH_1600 = 0xAC


class GyroRange(Enum):
    """Gyroscope range settings."""

    RANGE_2000_DPS = 0
    RANGE_1000_DPS = 1
    RANGE_500_DPS = 2
    RANGE_250_DPS = 3
    RANGE_125_DPS = 4


class GyroBandwidth(Enum):
    """Gyroscope filter bandwidth settings."""

    BANDWIDTH_2000 = 0
    # BANDWIDTH_2000 = 1
    BANDWIDTH_1000 = 2
    BANDWIDTH_400 = 3
    BANDWIDTH_200 = 4
    BANDWIDTH_100 = 5
    # BANDWIDTH_200 = 6
    # BANDWIDTH_100 = 7


ACC_SENSITIVITY_MAP = {
    AccRange.RANGE_3G: 10920,
    AccRange.RANGE_6G: 5460,
    AccRange.RANGE_12G: 2730,
    AccRange.RANGE_24G: 1365,
}

GYRO_SENSITIVITY_MAP = {
    GyroRange.RANGE_2000_DPS: 16.384,
    GyroRange.RANGE_1000_DPS: 32.768,
    GyroRange.RANGE_500_DPS: 65.536,
    GyroRange.RANGE_250_DPS: 131.072,
    GyroRange.RANGE_125_DPS: 262.144,
}


class BMI088:
    """BMI088 sensor interface class."""

    def __init__(
        self,
        i2c_bus,
        acc_range: AccRange = AccRange.RANGE_6G,
        acc_bandwidth: AccBandwidth = AccBandwidth.BANDWIDTH_100,
        gyro_range: GyroRange = GyroRange.RANGE_2000_DPS,
        gyro_bandwidth: GyroBandwidth = GyroBandwidth.BANDWIDTH_2000,
    ):
        """Initialize the BMI088 sensor interface."""
        self.bus = SMBus(i2c_bus)
        self.acc_range = acc_range
        self.acc_bandwidth = acc_bandwidth
        self.gyro_range = gyro_range
        self.gyro_bandwidth = gyro_bandwidth
        self._start()

    def _start(self):
        """Start the BMI088 sensor."""
        self.bus.write_byte_data(ACC_ADDRESS, 0x40, self.acc_bandwidth.value)
        self.bus.write_byte_data(ACC_ADDRESS, 0x41, self.acc_range.value)

        self.bus.write_byte_data(GYRO_ADDRESS, 0x0F, self.gyro_range.value)
        self.bus.write_byte_data(GYRO_ADDRESS, 0x10, self.gyro_bandwidth.value)

        self.bus.write_byte_data(ACC_ADDRESS, ACC_ENABLE_ADDRESS, ACC_ON)

    def read_acceleration(self, m_per_s2=False):
        """Read acceleration data from the BMI088 accelerometer.

        Outputs acceleration in g by default.

        Args:
            m_per_s2 (bool): If True, returns acceleration in meters per second squared.

        Returns:
            Tuple of acceleration values in the X, Y, and Z axes.

        """
        x_lsb = self.bus.read_byte_data(ACC_ADDRESS, ACC_X_LSB)
        x_msb = self.bus.read_byte_data(ACC_ADDRESS, ACC_X_MSB)

        x_lsb = self.bus.read_byte_data(ACC_ADDRESS, ACC_X_LSB)
        x_msb = self.bus.read_byte_data(ACC_ADDRESS, ACC_X_MSB)

        y_lsb = self.bus.read_byte_data(ACC_ADDRESS, ACC_Y_LSB)
        y_msb = self.bus.read_byte_data(ACC_ADDRESS, ACC_Y_MSB)
        z_lsb = self.bus.read_byte_data(ACC_ADDRESS, ACC_Z_LSB)
        z_msb = self.bus.read_byte_data(ACC_ADDRESS, ACC_Z_MSB)

        # print(z_msb, z_lsb)

        x = (np.array(((x_msb << 8) | x_lsb)).astype(np.int16)).astype(float)
        y = (np.array(((y_msb << 8) | y_lsb)).astype(np.int16)).astype(float)
        z = (np.array(((z_msb << 8) | z_lsb)).astype(np.int16)).astype(float)

        x /= ACC_SENSITIVITY_MAP[self.acc_range]
        y /= ACC_SENSITIVITY_MAP[self.acc_range]
        z /= ACC_SENSITIVITY_MAP[self.acc_range]

        if m_per_s2:
            x *= 9.80665
            y *= 9.80665
            z *= 9.80665

        return x, y, z

    def read_acceleration_block(self, m_per_s=False):
        """Read acceleration data from the BMI088 accelerometer using block read.

        Outputs acceleration in g by default.

        Args:
            m_per_s (bool): If True, returns acceleration in meters per second squared.

        Returns:
            Tuple of acceleration values in the X, Y, and Z axes.

        """
        block = self.bus.read_i2c_block_data(ACC_ADDRESS, ACC_X_LSB, 6)
        x = (np.array(((block[1] << 8) | block[0])).astype(np.int16)).astype(float)
        y = (np.array(((block[3] << 8) | block[2])).astype(np.int16)).astype(float)
        z = (np.array(((block[5] << 8) | block[4])).astype(np.int16)).astype(float)

        x /= ACC_SENSITIVITY_MAP[self.acc_range]
        y /= ACC_SENSITIVITY_MAP[self.acc_range]
        z /= ACC_SENSITIVITY_MAP[self.acc_range]

        if m_per_s:
            x *= 9.80665
            y *= 9.80665
            z *= 9.80665

        return x, y, z

    def read_gyroscope(self, deg_per_sec=False):
        """Read gyroscope data from the BMI088 gyroscope.

        Outputs angular velocity in radians per second by default.

        Args:
            deg_per_sec (bool): If True, returns angular velocity in degrees per second.

        Returns:
            Tuple of angular velocity values in the X, Y, and Z axes.

        """
        x_lsb = self.bus.read_byte_data(GYRO_ADDRESS, GYRO_RATE_X_LSB)
        x_msb = self.bus.read_byte_data(GYRO_ADDRESS, GYRO_RATE_X_MSB)
        y_lsb = self.bus.read_byte_data(GYRO_ADDRESS, GYRO_RATE_Y_LSB)
        y_msb = self.bus.read_byte_data(GYRO_ADDRESS, GYRO_RATE_Y_MSB)
        z_lsb = self.bus.read_byte_data(GYRO_ADDRESS, GYRO_RATE_Z_LSB)
        z_msb = self.bus.read_byte_data(GYRO_ADDRESS, GYRO_RATE_Z_MSB)

        x = (np.array(((x_msb << 8) | x_lsb)).astype(np.int16)).astype(float)
        y = (np.array(((y_msb << 8) | y_lsb)).astype(np.int16)).astype(float)
        z = (np.array(((z_msb << 8) | z_lsb)).astype(np.int16)).astype(float)

        x /= GYRO_SENSITIVITY_MAP[self.gyro_range]
        y /= GYRO_SENSITIVITY_MAP[self.gyro_range]
        z /= GYRO_SENSITIVITY_MAP[self.gyro_range]

        if not deg_per_sec:
            x = np.deg2rad(x)
            y = np.deg2rad(y)
            z = np.deg2rad(z)

        return x, y, z

    def read_temperature(self):
        """Read temperature data from the BMI088 sensor.

        Returns:
            Temperature in degrees Celsius.
    
        """
        temp_msb = self.bus.read_byte_data(ACC_ADDRESS, TEMP_MSB)
        temp_lsb = self.bus.read_byte_data(ACC_ADDRESS, TEMP_LSB)

        _temp = (temp_msb << 3) | (temp_lsb >> 5)
        temp = _temp * 0.125 + 23
        return temp

    def close(self):
        """Close the I2C bus."""
        self.bus.close()
