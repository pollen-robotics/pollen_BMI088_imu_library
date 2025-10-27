"""BMI088 sensor interface module."""

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


class BMI088:
    """BMI088 sensor interface class."""

    def __init__(self, i2c_bus):
        """Initialize the BMI088 sensor interface."""
        self.bus = SMBus(i2c_bus)
        self._start()

    def _start(self):
        """Start the BMI088 sensor."""
        self.bus.write_byte_data(ACC_ADDRESS, 0x7D, 0x04)

    def read_acceleration(self):
        """Read acceleration data from the BMI088 accelerometer."""
        x_lsb = self.bus.read_byte_data(ACC_ADDRESS, ACC_X_LSB)
        x_msb = self.bus.read_byte_data(ACC_ADDRESS, ACC_X_MSB)
        y_lsb = self.bus.read_byte_data(ACC_ADDRESS, ACC_Y_LSB)
        y_msb = self.bus.read_byte_data(ACC_ADDRESS, ACC_Y_MSB)
        z_lsb = self.bus.read_byte_data(ACC_ADDRESS, ACC_Z_LSB)
        z_msb = self.bus.read_byte_data(ACC_ADDRESS, ACC_Z_MSB)

        x = (x_msb << 8) | x_lsb
        y = (y_msb << 8) | y_lsb
        z = (z_msb << 8) | z_lsb

        return x, y, z

    def read_gyroscope(self):
        """Read gyroscope data from the BMI088 gyroscope."""
        x_lsb = self.bus.read_byte_data(GYRO_ADDRESS, GYRO_RATE_X_LSB)
        x_msb = self.bus.read_byte_data(GYRO_ADDRESS, GYRO_RATE_X_MSB)
        y_lsb = self.bus.read_byte_data(GYRO_ADDRESS, GYRO_RATE_Y_LSB)
        y_msb = self.bus.read_byte_data(GYRO_ADDRESS, GYRO_RATE_Y_MSB)
        z_lsb = self.bus.read_byte_data(GYRO_ADDRESS, GYRO_RATE_Z_LSB)
        z_msb = self.bus.read_byte_data(GYRO_ADDRESS, GYRO_RATE_Z_MSB)

        x = (x_msb << 8) | x_lsb
        y = (y_msb << 8) | y_lsb
        z = (z_msb << 8) | z_lsb

        return x, y, z

    def close(self):
        """Close the I2C bus."""
        self.bus.close()
