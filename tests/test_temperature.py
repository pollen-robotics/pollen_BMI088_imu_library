"""Tests for BMI088.read_temperature."""

import pytest

from bmi088.bmi088 import BMI088
from bmi088.params import TEMP_LSB, TEMP_MSB


class _FakeBus:
    def __init__(self, msb: int, lsb: int) -> None:
        self._regs = {TEMP_MSB: msb, TEMP_LSB: lsb}

    def read_byte_data(self, _address: int, register: int) -> int:
        return self._regs[register]


def _read(raw11: int) -> float:
    imu = BMI088.__new__(BMI088)  # skip __init__: no I2C bus here
    imu.bus = _FakeBus(raw11 >> 3, (raw11 & 0x7) << 5)
    return imu.read_temperature()


@pytest.mark.parametrize(
    ("raw11", "celsius"),
    [
        (0, 23.0),
        (56, 30.0),
        (1023, 150.875),
        (2047, 22.875),  # two's complement -1
        (1024, -105.0),  # two's complement -1024
    ],
)
def test_read_temperature(raw11: int, celsius: float) -> None:
    """Raw 11-bit values follow the datasheet's two's complement."""
    assert _read(raw11) == celsius
