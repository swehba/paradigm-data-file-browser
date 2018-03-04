import os
import json
from geolocation import Geolocation


class ActionDataFile:

    @classmethod
    def create(cls, directory: str, file_name: str):

        # Make sure the file is actually a file and not a directory.
        path = os.path.join(directory, file_name)
        if not os.path.isfile(path):
            return

        # Make sure the file has a .JSON extension.
        _, extension = os.path.splitext(path)
        if not extension.lower() == '.json':
            return

        # Open the file and read its contents as JSON.
        f = None
        # noinspection PyBroadException
        try:
            f = open(path, 'r')
            data = json.load(f)
        except:
            print(f"ERROR: couldn't load JSON from file [{path}]")
            return
        finally:
            if f:
                f.close()

        return ActionDataFile(path, data)

    def __init__(self, path: str, json_data: dict):
        self.path = path
        self.size = os.path.getsize(path)
        self.action_type = json_data.get('actionType', 'unknown')
        self.sensor_location = json_data.get('sensorLocation', 'unknown')
        self.note = json_data.get('note', '')
        self.start_time = json_data.get('startTime', '')
        self.end_time = json_data.get('endTime', '')
        self.handedness = json_data.get('handedness', '')
        self.sampling_frequency = json_data.get('samplingFrequency', 0)
        self.sampling_period = json_data.get('samplingPeriod', 0)
        self.watch_model = json_data.get('watchModel', '')
        self.distance = json_data.get('distance', '')
        self.phone = json_data.get('phone', '')
        geolocation = json_data.get('geolocation')
        if geolocation:
            lat = geolocation.get('latitude', 0.0)
            lon = geolocation.get('longitude', 0.0)
            alt = geolocation.get('altitude', 0.0)
            self.geolocation = Geolocation(lat, lon, alt)
        else:
            self.geolocation = Geolocation()

        self.gyro_sample_count = 0
        gyro_data = json_data.get('gyroData')
        if gyro_data:
            self.gyro_sample_count = len(gyro_data)

        self.accel_sample_count = 0
        accel_data = json_data.get('accelData')
        if accel_data:
            self.accel_sample_count = len(accel_data)

    def __repr__(self):
        return f'{self.name_noext}, size={self.size}, action_type={self.action_type}, ' \
               f'sensor_location={self.sensor_location},gyro_samples={self.gyro_sample_count}, ' \
               f'accel_samples={self.accel_sample_count}, start={self.start_time}, end={self.end_time}, ' \
               f'note={self.note}'

    @property
    def directory(self):
        head, tail = os.path.split(self.path)
        return head

    @property
    def name(self):
        head, tail = os.path.split(self.path)
        return tail

    @property
    def name_noext(self):
        name, ext = os.path.splitext(self.name)
        return name
