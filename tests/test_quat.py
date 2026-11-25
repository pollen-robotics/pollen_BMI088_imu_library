"""Tests for BMI088.get_quat."""

import numpy as np
from ahrs.filters import Madgwick

from bmi088.bmi088 import BMI088

ACC = (0.1, 0.2, 9.7)
GYR = (0.01, -0.02, 0.03)


class _CountingBus:
    def __init__(self) -> None:
        self.reads = 0

    def read_i2c_block_data(
        self, _address: int, _register: int, _length: int
    ) -> list[int]:
        self.reads += 1
        return [0] * 6


def _imu() -> BMI088:
    imu = BMI088.__new__(BMI088)  # skip __init__: no I2C bus here
    imu.bus = _CountingBus()
    imu.q = np.array([1, 0, 0, 0])
    imu.madgwick = Madgwick()
    return imu


def test_given_readings_skip_the_bus() -> None:
    """Passing acc and gyr reads nothing and matches a direct filter update."""
    imu = _imu()
    q = imu.get_quat(0.02, acc=ACC, gyr=GYR)
    assert imu.bus.reads == 0
    expected = Madgwick().updateIMU(q=np.array([1, 0, 0, 0]), acc=ACC, gyr=GYR, dt=0.02)
    assert np.allclose(q, expected)
