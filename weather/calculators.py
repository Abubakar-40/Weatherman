from weather.models import WeatherReading, YearlySummary


class YearlySummaryCalculator:
    def calculate(self, readings: list[WeatherReading]):
        readings_with_max_temp = [reading for reading in readings if reading.max_temp is not None]
        readings_with_min_temp = [reading for reading in readings if reading.min_temp is not None]
        readings_with_max_humidity = [reading for reading in readings if reading.max_humidity is not None]

        if not readings_with_max_temp or not readings_with_min_temp or not readings_with_max_humidity:
            raise ValueError("Not enough weather data available for the requested year.")

        highest_reading = max(readings_with_max_temp, key=lambda reading: reading.max_temp)
        lowest_reading = min(readings_with_min_temp, key=lambda reading: reading.min_temp)
        most_humid_reading = max(readings_with_max_humidity, key=lambda reading: reading.max_humidity)

        summary = YearlySummary(
            highest_temp=highest_reading.max_temp,
            highest_temp_date=highest_reading.reading_date,
            lowest_temp=lowest_reading.min_temp,
            lowest_temp_date=lowest_reading.reading_date,
            most_humid_day_humidity=most_humid_reading.max_humidity,
            most_humid_day_date=most_humid_reading.reading_date,
        )

        return summary