import pickle # noqa
import time

import numpy as np

from bmi088 import BMI088
from bmi088.params import AccBandwidth, AccRange, GyroBandwidth, GyroRange

sensor = BMI088(
    i2c_bus=4,
    gyro_range=GyroRange.RANGE_500_DPS,
    gyro_bandwidth=GyroBandwidth.BANDWIDTH_100,
    acc_range=AccRange.RANGE_3G,
    acc_bandwidth=AccBandwidth.BANDWIDTH_200,
)
dt = 1 / 200
t0 = time.time()
data = []
last_t = time.time()
i = 0
freqs = []

for i in range(10):
    acceleration = sensor.read_acceleration()
    gyroscope = sensor.read_gyroscope()
try:
    while True:
        t = time.time() - t0
        loop_start = time.time()

        acceleration = sensor.read_acceleration()
        if i % 25 == 0:
            print(acceleration[3])
        gyroscope = sensor.read_gyroscope()

        data.append([t, list(acceleration), list(gyroscope)])

        if t > 10.0:
            break

        i += 1
        freq = 1 / (time.time() - last_t)
        freqs.append(freq)
        # if i%10 == 0:
        #     print(f"Frequency: {freq:.2f} Hz")

        last_t = time.time()
        loop_took = time.time() - loop_start
        time.sleep(max(0, dt - loop_took))
        # print("==")
except KeyboardInterrupt:
    pass

print("average and std frequency:", np.mean(freqs), np.std(freq))
print("Stopping logging")
print("Saving data to log.pkl")
with open("log.pkl", "wb") as f:
    pickle.dump(data, f)
