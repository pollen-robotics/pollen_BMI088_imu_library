"""BMI088 sensor interface module."""

import numpy as np
from smbus3 import SMBus
import time
from ahrs.filters import Madgwick

from bmi088.params import (
    ACC_ADDRESS,
    ACC_ENABLE_ADDRESS,
    ACC_ON,
    ACC_POWER_CONF,
    ACC_SOFT_RESET,
    ACC_SENSITIVITY_MAP,
    ACC_X_LSB,
    GYRO_ADDRESS,
    GYRO_RATE_X_LSB,
    GYRO_SENSITIVITY_MAP,
    TEMP_LSB,
    TEMP_MSB,
    AccBandwidth,
    AccRange,
    GyroBandwidth,
    GyroRange,
)


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
        self.q = np.array([1, 0, 0, 0])
        self.madgwick = Madgwick()
        self._start()

    def _start(self):
        """Start the BMI088 sensor."""

        # soft reset

        # self.bus.write_byte_data(ACC_ADDRESS, ACC_SOFT_RESET, 0xB6)
        # time.sleep(0.001)

        self.bus.write_byte_data(ACC_ADDRESS, 0x40, self.acc_bandwidth.value)
        self.bus.write_byte_data(ACC_ADDRESS, 0x41, self.acc_range.value)

        self.bus.write_byte_data(GYRO_ADDRESS, 0x0F, self.gyro_range.value)
        self.bus.write_byte_data(GYRO_ADDRESS, 0x10, self.gyro_bandwidth.value)

        self.bus.write_byte_data(ACC_ADDRESS, ACC_POWER_CONF, 0x00)
        self.bus.write_byte_data(ACC_ADDRESS, ACC_ENABLE_ADDRESS, ACC_ON)

    def read_acceleration(self, m_per_s2=False):
        """Read acceleration data from the BMI088 accelerometer using block read.

        Outputs acceleration in g by default.

        Args:
            m_per_s2 (bool): If True, returns acceleration in meters per second squared.

        Returns:
            Tuple of acceleration values in the X, Y, and Z axes.

        """
        block = self.bus.read_i2c_block_data(ACC_ADDRESS, ACC_X_LSB, 6)
        x = (np.array(((block[1] << 8) | block[0])).astype(np.int16)).astype(float)
        y = (np.array(((block[3] << 8) | block[2])).astype(np.int16)).astype(float)
        z = (np.array(((block[5] << 8) | block[4])).astype(np.int16)).astype(float)
        hex_z = hex((np.array(((block[5] << 8) | block[4])).astype(np.int16)))

        x /= ACC_SENSITIVITY_MAP[self.acc_range]
        y /= ACC_SENSITIVITY_MAP[self.acc_range]
        z /= ACC_SENSITIVITY_MAP[self.acc_range]

        if m_per_s2:
            x *= 9.80665
            y *= 9.80665
            z *= 9.80665

        return x, y, z, hex_z

    def read_gyroscope(self, deg_per_s=False):
        """Read gyroscope data from the BMI088 gyroscope using block read.

        Outputs angular velocity in radians per second by default.

        Args:
            deg_per_s (bool): If True, returns angular velocity in degrees per second.

        Returns:
            Tuple of angular velocity values in the X, Y, and Z axes.

        """
        block = self.bus.read_i2c_block_data(GYRO_ADDRESS, GYRO_RATE_X_LSB, 6)
        x = (np.array(((block[1] << 8) | block[0])).astype(np.int16)).astype(float)
        y = (np.array(((block[3] << 8) | block[2])).astype(np.int16)).astype(float)
        z = (np.array(((block[5] << 8) | block[4])).astype(np.int16)).astype(float)

        x /= GYRO_SENSITIVITY_MAP[self.gyro_range]
        y /= GYRO_SENSITIVITY_MAP[self.gyro_range]
        z /= GYRO_SENSITIVITY_MAP[self.gyro_range]

        if not deg_per_s:
            x = np.deg2rad(x)
            y = np.deg2rad(y)
            z = np.deg2rad(z)

        return x, y, z

    def get_quat(self, dt: float):
        """Get orientation quaternion using Madgwick filter."""
        madgwick = Madgwick()
        acc = self.read_acceleration()[:3]
        gyro = self.read_gyroscope()[:3]
        self.q = madgwick.updateIMU(q=self.q, acc=acc, gyr=gyro, dt=dt)
        return self.q

    def read_temperature(self):
        """Read temperature data from the BMI088 sensor.

        Returns:
            Temperature in degrees Celsius.

        """
        temp_lsb = self.bus.read_byte_data(ACC_ADDRESS, TEMP_LSB)
        temp_msb = self.bus.read_byte_data(ACC_ADDRESS, TEMP_MSB)

        _temp = (temp_msb << 3) | (temp_lsb >> 5)
        temp = _temp * 0.125 + 23
        return temp

    def close(self):
        """Close the I2C bus."""
        self.bus.close()
