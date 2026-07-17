import calendar

import pandas as pd

from weather.classes import Reports, WeatherRecord


class WeatherService:
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
            data_frame = pd.read_csv(file_path, skipinitialspace=True)
            data_frame.columns = [column.strip() for column in data_frame.columns]
            date_column = data_frame.columns[0]

            for _, row in data_frame.iterrows():
                reading = WeatherRecord(
                    date=pd.to_datetime(row[date_column]).date(),
                    max_temp=self.parse_optional_float(row.get("Max TemperatureC")),
                    min_temp=self.parse_optional_float(row.get("Min TemperatureC")),
                    max_humidity=self.parse_optional_float(row.get("Max Humidity")),
                    mean_humidity=self.parse_optional_float(row.get("Mean Humidity")),
                )
                readings.append(reading)

        return readings

    def parse_optional_float(self, value):
        if pd.isna(value):
            return None

        return float(value)

    def calculate_yearly_summary(self, readings):
        filtered = self.filter_readings(readings, "max_humidity")

        if filtered is None:
            return None

        max_temp, min_temp, humidity = filtered

        highest_reading = max(max_temp, key=lambda reading: reading.max_temp)
        lowest_reading = min(min_temp, key=lambda reading: reading.min_temp)
        most_humid_reading = max(humidity, key=lambda reading: reading.max_humidity)

        return Reports(
            highest=highest_reading.max_temp,
            highest_date=highest_reading.date,
            lowest=lowest_reading.min_temp,
            lowest_date=lowest_reading.date,
            humidity=most_humid_reading.max_humidity,
            humidity_date=most_humid_reading.date,
        )

    def calculate_monthly_average(self, readings):
        filtered = self.filter_readings(readings, "mean_humidity")

        if filtered is None:
            return None

        max_temp, min_temp, humidity = filtered

        max_temps = [reading.max_temp for reading in max_temp]
        min_temps = [reading.min_temp for reading in min_temp]
        mean_humidities = [reading.mean_humidity for reading in humidity]

        return Reports(
            highest=sum(max_temps) / len(max_temps),
            lowest=sum(min_temps) / len(min_temps),
            humidity=sum(mean_humidities) / len(mean_humidities),
        )

    def filter_readings(self, readings, humidity_field):
        max_temp = [reading for reading in readings if reading.max_temp is not None]
        min_temp = [reading for reading in readings if reading.min_temp is not None]
        humidity = [reading for reading in readings if getattr(reading, humidity_field) is not None]

        if not max_temp or not min_temp or not humidity:
            return None

        return max_temp, min_temp, humidity
