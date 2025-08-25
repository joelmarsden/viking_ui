import random
import time
import math
from dataclasses import dataclass
from typing import Dict


@dataclass
class SensorReading:
    temperature: float
    heart_rate: int
    gyroscope: Dict[str, float]
    accelerometer: Dict[str, float]
    gforce: float
    timestamp: float


SIMULATE = True

if not SIMULATE:

    from mpu6050 import mpu6050
    from smbus2 import SMBus
    from mlx90614 import MLX90614
    from src.pulsesensor import Pulsesensor

    class SensorService:

        def __init__(self):
            self.bus = SMBus(1)
            self.mpu = mpu6050(0x68)
            self.mlx = MLX90614(self.bus, address=0x5A)
            self.pulse = Pulsesensor(0, 1, 860)
            self.pulse.startAsyncBPM()

        def get_current_reading(self) -> SensorReading:
            accelerometer_data = self.mpu.get_accel_data()
            gyroscope_data = self.mpu.get_gyro_data()
            gyro_temperature = self.mpu.get_temp()

            ambient_temp = self.mlx.get_amb_temp()
            object_temp = self.mlx.get_obj_temp()

            temperature = round(ambient_temp, 1)
            heart_rate = round(self.pulse.BPM, 0)

            gyroscope = {
                'x': round(gyroscope_data['x'], 3),
                'y': round(gyroscope_data['y'], 3),
                'z': round(gyroscope_data['z'], 3)
            }

            accelerometer = {
                'x': round(accelerometer_data['x'], 3),
                'y': round(accelerometer_data['y'], 3),
                'z': round(accelerometer_data['z'], 3)
            }

            gforce = round(math.sqrt(
                accelerometer['x'] ** 2 +
                accelerometer['y'] ** 2 +
                accelerometer['z'] ** 2
            ) / 9.8, 2)

            return SensorReading(
                temperature=temperature,
                heart_rate=heart_rate,
                gyroscope=gyroscope,
                accelerometer=accelerometer,
                gforce=gforce,
                timestamp=time.time()
            )
else:
    class SensorService:
        """Simulates sensor data """

        def __init__(self):
            self.base_temp = 36.5
            self.base_hr = 75

        def get_current_reading(self) -> SensorReading:
            # Simulate realistic sensor data with some variation
            temperature = round(self.base_temp + random.uniform(-2, 4), 1)
            heart_rate = self.base_hr + random.randint(-15, 40)

            gyroscope = {
                'x': round(random.uniform(-10, 10), 2),
                'y': round(random.uniform(-10, 10), 2),
                'z': round(random.uniform(-10, 10), 2)
            }

            accelerometer = {
                'x': round(random.uniform(-2, 2), 2),
                'y': round(random.uniform(-2, 2), 2),
                'z': round(9.8 + random.uniform(-1, 1), 2)  # gravity + variation
            }

            # Calculate G-Force from accelerometer data
            gforce = round(math.sqrt(
                accelerometer['x'] ** 2 +
                accelerometer['y'] ** 2 +
                accelerometer['z'] ** 2
            ) / 9.8, 2)

            return SensorReading(
                temperature=temperature,
                heart_rate=heart_rate,
                gyroscope=gyroscope,
                accelerometer=accelerometer,
                gforce=gforce,
                timestamp=time.time()
            )
