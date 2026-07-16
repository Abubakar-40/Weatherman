from weather.models import MonthlyAverages, WeatherReading, YearlySummary


class YearlySummaryCalculator:
    def calculate(self, readings: list[WeatherReading]):
        readings_with_max_temp = [reading for reading in readings if reading.max_temp is not None]
        readings_with_min_temp = [reading for reading in readings if reading.min_temp is not None]
        readings_with_max_humidity = [reading for reading in readings if reading.max_humidity is not None]

        if not readings_with_max_temp or not readings_with_min_temp or not readings_with_max_humidity:
            return None

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

class MonthlyAverageCalculator:
    def calculate(self, readings: list[WeatherReading]):
        max_temps = [reading.max_temp for reading in readings if reading.max_temp is not None]
        min_temps = [reading.min_temp for reading in readings if reading.min_temp is not None]
        mean_humidities = [reading.mean_humidity for reading in readings if reading.mean_humidity is not None]

        if not max_temps or not min_temps or not mean_humidities:
            return None

        averages = MonthlyAverages(
            avg_highest_temp=sum(max_temps) / len(max_temps),
            avg_lowest_temp=sum(min_temps) / len(min_temps),
            avg_mean_humidity=sum(mean_humidities) / len(mean_humidities),
        )

        return averages