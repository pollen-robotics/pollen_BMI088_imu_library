from enum import Enum # noqa

ACC_ADDRESS = 0x18
GYRO_ADDRESS = 0x69

ACC_ENABLE_ADDRESS = 0x7D
ACC_POWER_CONF = 0x7D
ACC_SOFT_RESET = 0x7E

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
    """Gyroscope filter bandwidth settings.

    Note : The commented values are found in the docs.
    """

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
