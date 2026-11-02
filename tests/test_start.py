"""Tests for BMI088 start-up configuration."""

from types import SimpleNamespace

from bmi088.bmi088 import BMI088
from bmi088.params import ACC_ADDRESS, ACC_ON


class _RecordingBus:
    def __init__(self) -> None:
        self.writes: list[tuple[int, int, int]] = []

    def write_byte_data(self, address: int, register: int, value: int) -> None:
        self.writes.append((address, register, value))


def test_start_puts_accelerometer_in_normal_mode() -> None:
    """ACC_PWR_CONF (0x7C) goes active, then ACC_PWR_CTRL (0x7D) turns it on."""
    imu = BMI088.__new__(BMI088)  # skip __init__: no I2C bus here
    imu.bus = _RecordingBus()
    setting = SimpleNamespace(value=0)
    imu.acc_bandwidth = imu.acc_range = imu.gyro_range = imu.gyro_bandwidth = setting

    imu._start()

    acc_power = [(r, v) for a, r, v in imu.bus.writes if a == ACC_ADDRESS and r >= 0x7C]
    assert acc_power == [(0x7C, 0x00), (0x7D, ACC_ON)]
