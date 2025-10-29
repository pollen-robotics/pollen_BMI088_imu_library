"""pip install FramesViewer scipy."""

import argparse
import pickle
import socket
import time
from queue import Queue
from threading import Thread

import numpy as np
from FramesViewer import Viewer
from scipy.spatial.transform import Rotation as R


class IMUClient:
    def __init__(self, host, port=1234, freq=30):
        self.host = host
        self.port = port
        self.freq = freq
        self.client_socket = socket.socket()
        self.connected = False
        while not self.connected:
            try:
                self.client_socket.connect((self.host, self.port))
                self.connected = True
            except Exception as e:
                print(e)
                time.sleep(0.5)
        self.imu_queue = Queue(maxsize=1)
        self.last_imu = {
            "acceleration": [0, 0, 0],
            "gyroscope": [0, 0, 0],
            "quaternion": [1, 0, 0, 0],
        }

        Thread(target=self.imu_worker, daemon=True).start()

    def imu_worker(self):
        while True:
            try:
                data = self.client_socket.recv(1024)  # receive response
                data = pickle.loads(data)

                self.imu_queue.put(data)
            except:
                print("missed imu")

            time.sleep(1 / self.freq)

    def get_imu(self):
        try:
            self.last_imu = self.imu_queue.get(False)
        except:
            # self.last_imu = {
            #     "acceleration": [0, 0, 9.81],
            #     "gyroscope": [0, 0, 0],
            # }
            pass

        return self.last_imu


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--ip", type=str, required=True, help="IP address of the robot")
    args = parser.parse_args()

    client = IMUClient(args.ip)

    fv = Viewer()
    fv.start()
    pose = np.eye(4)
    original_pose = [0.1, 0.1, 0.1]
    pose[:3, 3] = original_pose.copy()
    dt = 1 / 10
    acc_values = []
    try:
        i = 0
        while True:
            data = client.get_imu()
            acc = data["acceleration"]
            gyro = data["gyroscope"]
            quat = data["quaternion"]

            try:
                # pose[:3, 3] = np.array(original_pose).copy()
                acc_values.append(acc)
                print(i, np.around(acc, 3))
                pose[:3, 3] = 10*np.array(acc - np.array([0, 0, 9.81])) * dt * dt
                delta_angle = np.array(gyro) * dt
                delta_rot = R.from_euler("xyz", delta_angle, degrees=False)
                rot_mat = delta_rot.as_matrix() @ pose[:3, :3]
                # pose[:3, :3] = rot_mat
                fv.push_frame(pose, "pose")
                i += 1
            except Exception as e:
                print("error", e)
                pass
            time.sleep(dt)
    except KeyboardInterrupt:
        pass


    # plot acc values
    import matplotlib.pyplot as plt

    plt.plot(acc_values)
    plt.xlabel("Time (s)")
    plt.ylabel("Acceleration (m/s^2)")
    plt.title("IMU Acceleration Data")
    plt.show()