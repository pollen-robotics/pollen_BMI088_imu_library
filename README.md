# Pollen BMI088 IMU library

A simple library to get data from the BMI088 IMU in i2c

## Installation 

From PyPi: 

`pip install pollen_bmi088_imu_library`

From the repo:

`pip install -e .`

## Usage 

Import and use the library like this 

```python
from bmi088 import BMI088

accelerometer = imu.read_accelerometer(m_per_s2=...)

gyroscope = imu.read_gyroscope(deg_per_s=...)

quat = imu.get_quat(dt)

```

## License

Apache 2.0, see [LICENSE](LICENSE).