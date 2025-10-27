from bmi088 import BMI088

if __name__ == "__main__":
    sensor = BMI088(i2c_bus=4)

    acceleration = sensor.read_acceleration()
    print(
        f"Acceleration: X={acceleration[0]}, Y={acceleration[1]}, Z={acceleration[2]}"
    )

    gyroscope = sensor.read_gyroscope()
    print(f"Gyroscope: X={gyroscope[0]}, Y={gyroscope[1]}, Z={gyroscope[2]}")
