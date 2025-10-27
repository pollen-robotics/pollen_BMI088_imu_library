"""BMI088 sensor interface module."""

from enum import Enum

import numpy as np
from smbus3 import SMBus

ACC_ADDRESS = 0x18
GYRO_ADDRESS = 0x69

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


class AccRange(Enum):
    """Accelerometer range settings."""

    RANGE_3G = 3
    RANGE_6G = 6
    RANGE_12G = 12
    RANGE_24G = 24


class GyroRange(Enum):
    """Gyroscope range settings."""

    RANGE_2000_DPS = 2000
    RANGE_1000_DPS = 1000
    RANGE_500_DPS = 500
    RANGE_250_DPS = 250
    RANGE_125_DPS = 125


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
        gyro_range: GyroRange = GyroRange.RANGE_2000_DPS,
    ):
        """Initialize the BMI088 sensor interface."""
        self.bus = SMBus(i2c_bus)
        self.acc_range = acc_range
        self.gyro_range = gyro_range
        self._start()

    def _start(self):
        """Start the BMI088 sensor."""
        self.bus.write_byte_data(ACC_ADDRESS, 0x7D, 0x04)

    def read_acceleration(self, m_per_s=False):
        """Read acceleration data from the BMI088 accelerometer."""
        x_lsb = self.bus.read_byte_data(ACC_ADDRESS, ACC_X_LSB)
        x_msb = self.bus.read_byte_data(ACC_ADDRESS, ACC_X_MSB)
        y_lsb = self.bus.read_byte_data(ACC_ADDRESS, ACC_Y_LSB)
        y_msb = self.bus.read_byte_data(ACC_ADDRESS, ACC_Y_MSB)
        z_lsb = self.bus.read_byte_data(ACC_ADDRESS, ACC_Z_LSB)
        z_msb = self.bus.read_byte_data(ACC_ADDRESS, ACC_Z_MSB)

        x = np.int16((x_msb << 8) | x_lsb)
        y = np.int16((y_msb << 8) | y_lsb)
        z = np.int16((z_msb << 8) | z_lsb)

        x /= ACC_SENSITIVITY_MAP[self.acc_range]
        y /= ACC_SENSITIVITY_MAP[self.acc_range]
        z /= ACC_SENSITIVITY_MAP[self.acc_range]

        return x, y, z

    def read_gyroscope(self, m_per_s=False):
        """Read gyroscope data from the BMI088 gyroscope."""
        x_lsb = self.bus.read_byte_data(GYRO_ADDRESS, GYRO_RATE_X_LSB)
        x_msb = self.bus.read_byte_data(GYRO_ADDRESS, GYRO_RATE_X_MSB)
        y_lsb = self.bus.read_byte_data(GYRO_ADDRESS, GYRO_RATE_Y_LSB)
        y_msb = self.bus.read_byte_data(GYRO_ADDRESS, GYRO_RATE_Y_MSB)
        z_lsb = self.bus.read_byte_data(GYRO_ADDRESS, GYRO_RATE_Z_LSB)
        z_msb = self.bus.read_byte_data(GYRO_ADDRESS, GYRO_RATE_Z_MSB)

        x = np.int16((x_msb << 8) | x_lsb)
        y = np.int16((y_msb << 8) | y_lsb)
        z = np.int16((z_msb << 8) | z_lsb)

        x /= GYRO_SENSITIVITY_MAP[self.gyro_range]
        y /= GYRO_SENSITIVITY_MAP[self.gyro_range]
        z /= GYRO_SENSITIVITY_MAP[self.gyro_range]

        return x, y, z

    def close(self):
        """Close the I2C bus."""
        self.bus.close()
