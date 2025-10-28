import pickle
import time

from bmi088 import BMI088
from bmi088.bmi088 import AccBandwidth, AccRange, GyroBandwidth, GyroRange

sensor = BMI088(
    i2c_bus=4,
    gyro_range=GyroRange.RANGE_500_DPS,
    acc_range=AccRange.RANGE_3G,
    acc_bandwidth=AccBandwidth.BANDWIDTH_100,
    gyro_bandwidth=GyroBandwidth.BANDWIDTH_100,
)
dt = 1 / 50
t0 = time.time() - 1
data = []
try:
    while True:
        t = time.time() - t0
        if t > 1:
            acceleration = sensor.read_acceleration()
            gyroscope = sensor.read_gyroscope()
            data.append([t, list(acceleration), list(gyroscope)])
        time.sleep(dt)
        if t > 3.0:
            break
except KeyboardInterrupt:
    pass

print("Stopping logging")
print("Saving data to log.pkl")
with open("log.pkl", "wb") as f:
    pickle.dump(data, f)
