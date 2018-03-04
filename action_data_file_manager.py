from action_data_file import ActionDataFile
import os
from enum import Enum


class SortOrder(Enum):
    ascending = 1
    descending = 2


class SortBy(Enum):
    file_name = (lambda file: file.name)
    file_size = (lambda file: file.size)
    sample_count = (lambda file: file.gyro_sample_count)
    action_type = (lambda file: file.action_type)
    sensor_location = (lambda file: file.sensor_location)
    handedness = (lambda file: file.handedness)
    sampling_frequency = (lambda file: file.sampling_frequency)
    sampling_period = (lambda file: file.sampling_period)
    watch_model = (lambda file: file.watch_model)
    distance = (lambda file: file.distance)

    def __init__(self, sort_method):
        self.sort_method = sort_method


class ActionDataFileManager:
    def __init__(self):
        self.folder = ''
        self.data_files = []
        self.filtered_data_files = []
        self.next = 0

        self.sort_order = SortOrder.ascending
        self.sort_by = SortBy.file_name

        self.min_file_size = None
        self.max_file_size = None
        self.sensor_locations = None
        self.min_samples = None
        self.max_samples = None
        self.min_start = None
        self.action_types = None

    def clear_filters(self):
        self.min_file_size = None
        self.max_file_size = None
        self.sensor_locations = None
        self.min_samples = None
        self.max_samples = None
        self.min_start = None
        self.action_types = None

    def __iter__(self):
        self.next = 0
        self.filtered_data_files = []
        for file in self.data_files:
            if self.min_file_size and file.size < self.min_file_size:
                continue
            if self.max_file_size and file.size > self.max_file_size:
                continue
            if self.sensor_locations and file.sensor_location not in self.sensor_locations:
                continue
            if self.min_samples and (
                    file.gyro_sample_count < self.min_samples or file.accel_sample_count < self.min_samples):
                continue
            if self.max_samples and (
                    file.gyro_sample_count > self.max_samples or file.accel_sample_count > self.max_samples):
                continue
            if self.action_types and file.action_type not in self.action_types:
                continue

            self.filtered_data_files.append(file)

        self.filtered_data_files.sort(key=self.sort_by, reverse=(self.sort_order==SortOrder.descending))
        return self

    def __next__(self):
        if self.next >= len(self.filtered_data_files):
            raise StopIteration

        result = self.filtered_data_files[self.next]
        self.next += 1
        return result

    def load_folder(self, folder):
        self.data_files = []
        try:
            file_names = os.listdir(folder)
        except FileNotFoundError:
            print(f"ERROR: can't open folder [{folder}]")
            return

        self.folder = folder
        for file_name in file_names:
            data_file = ActionDataFile.create(folder, file_name)
            if data_file:
                self.data_files.append(data_file)
