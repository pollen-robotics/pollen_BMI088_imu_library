import pickle
import time

from bmi088 import BMI088

sensor = BMI088(i2c_bus=4)
dt = 1 / 50
t0 = time.time()
data = []
try:
    while True:
        t = time.time() - t0
        acceleration = sensor.read_acceleration()
        gyroscope = sensor.read_gyroscope()
        data.append([t, list(acceleration), list(gyroscope)])
        time.sleep(dt)
except KeyboardInterrupt:
    print("Stopping logging")
    print("Saving data to log.pkl")
    with open("log.pkl", "wb") as f:
        pickle.dump(data, f)
