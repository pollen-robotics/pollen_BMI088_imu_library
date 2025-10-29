import argparse
import pickle
import socket
import time
from threading import Thread

from bmi088 import BMI088


class IMUServer:
    def __init__(self):
        self.host = "0.0.0.0"
        self.port = 1234

        self.imu = BMI088(i2c_bus=4)

        self.server_socket = socket.socket()
        self.server_socket.setsockopt(
            socket.SOL_SOCKET, socket.SO_REUSEADDR, 1
        )  # enable address reuse

        self.server_socket.bind((self.host, self.port))
        self.stop = False

        Thread(target=self.run, daemon=True).start()

    def run(self):
        while not self.stop:
            self.server_socket.listen(1)
            conn, address = self.server_socket.accept()  # accept new connection
            print("Connection from: " + str(address))
            try:
                while True:
                    acc = self.imu.read_acceleration(m_per_s2=True)
                    gyro = self.imu.read_gyroscope(deg_per_sec=False)
                    quat = self.imu.get_quat(dt=1/30)
                    data = {"acceleration": acc, "gyroscope": gyro, "quaternion": quat}
                    data = pickle.dumps(data)
                    conn.send(data)  # send data to the client
                    time.sleep(1 / 30)
            except:
                pass

        self.server_socket.close()
        print("thread closed")
        time.sleep(1)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--pitch_bias", type=float, default=0, help="deg")
    args = parser.parse_args()
    imu_server = IMUServer()
    try:
        while True:
            time.sleep(0.01)
    except KeyboardInterrupt:
        print("Closing server")
        imu_server.stop = True

    time.sleep(2)
