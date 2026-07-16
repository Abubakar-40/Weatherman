import calendar

import pandas

from weather.models import WeatherReading


class WeatherDataParser:
    def __init__(self, data_dir):
        self.data_dir = data_dir

    def get_readings_for_year(self, year):
        return self.get_readings_matching(f"*_{year}_*.txt")

    def get_readings_for_month(self, year, month):
        month_abbreviation = calendar.month_abbr[month]

        return self.get_readings_matching(f"*_{year}_{month_abbreviation}.txt")

    def get_readings_matching(self, pattern):
        matching_files = sorted(self.data_dir.glob(pattern))
        readings = []

        for file_path in matching_files:
            data_frame = pandas.read_csv(file_path, skipinitialspace=True)
            data_frame.columns = [column.strip() for column in data_frame.columns]
            date_column = data_frame.columns[0]

            for _, row in data_frame.iterrows():
                reading = WeatherReading(
                    date=pandas.to_datetime(row[date_column]).date(),
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
