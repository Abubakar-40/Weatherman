from pathlib import Path

import pandas

from weather.models import WeatherReading


class WeatherDataParser:
    def __init__(self, data_dir: Path):
        self.data_dir = data_dir

    def get_readings_for_year(self, year: int):
        matching_files = sorted(self.data_dir.glob(f"*_{year}_*.txt"))
        readings = []

        for file_path in matching_files:
            readings.extend(self.parse_file(file_path))

        return readings

    def parse_file(self, file_path: Path):
        data_frame = pandas.read_csv(file_path, skipinitialspace=True)
        data_frame.columns = [column.strip() for column in data_frame.columns]
        date_column = data_frame.columns[0]

        readings = []
        for _, row in data_frame.iterrows():
            reading = WeatherReading(
                reading_date=pandas.to_datetime(row[date_column]).date(),
                max_temp=self.parse_optional_float(row.get("Max TemperatureC")),
                min_temp=self.parse_optional_float(row.get("Min TemperatureC")),
                max_humidity=self.parse_optional_float(row.get("Max Humidity")),
                mean_humidity=self.parse_optional_float(row.get("Mean Humidity")),
            )
            readings.append(reading)

        return readings

    def parse_optional_float(self, value):
        if pandas.isna(value):
            return None

        return float(value)