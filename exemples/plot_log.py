# plot log.pkl

import pickle
import matplotlib.pyplot as plt

with open("log.pkl", "rb") as f:
    data = pickle.load(f)

# data = data[2:]
# print(len(data))
# exit()

times = [d[0] for d in data]
acc_x = [d[1][0] - data[0][1][0] for d in data]
acc_y = [d[1][1] - data[0][1][1] for d in data]
acc_z = [d[1][2] - data[0][1][2] for d in data]
gyro_x = [d[2][0] - data[0][2][0] for d in data]
gyro_y = [d[2][1] - data[0][2][1] for d in data]
gyro_z = [d[2][2] - data[0][2][2] for d in data]
# temp = [d[3] for d in data]
plt.figure(figsize=(10, 12))
plt.subplot(2, 1, 1)
plt.plot(times, acc_x, label="Acc X")
plt.plot(times, acc_y, label="Acc Y")
plt.plot(times, acc_z, label="Acc Z")
plt.title("Acceleration")
plt.xlabel("Time (s)")
plt.ylabel("Acceleration (m/s²)")
plt.legend()

plt.subplot(2, 1, 2)
plt.plot(times, gyro_x, label="Gyro X")
plt.plot(times, gyro_y, label="Gyro Y")
plt.plot(times, gyro_z, label="Gyro Z")
plt.title("Gyroscope")
plt.xlabel("Time (s)")
plt.ylabel("Angular Velocity (rad/s)")
plt.legend()

# plt.subplot(3, 1, 3)
# plt.plot(times, temp, label="Temperature", color="tab:orange")
# plt.title("Temperature")
# plt.xlabel("Time (s)")
# plt.ylabel("Temperature (°C)")
# plt.legend()

plt.tight_layout()
plt.show()
