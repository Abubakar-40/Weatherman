from weather.models import ReportResult


class Calculator:
    def calculate_yearly_summary(self, readings):
        filtered = self.filter_readings(readings, "max_humidity")

        if filtered is None:
            return None

        readings_with_max_temp, readings_with_min_temp, readings_with_humidity = filtered

        highest_reading = max(readings_with_max_temp, key=lambda reading: reading.max_temp)
        lowest_reading = min(readings_with_min_temp, key=lambda reading: reading.min_temp)
        most_humid_reading = max(readings_with_humidity, key=lambda reading: reading.max_humidity)

        return ReportResult(
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

        readings_with_max_temp, readings_with_min_temp, readings_with_humidity = filtered

        max_temps = [reading.max_temp for reading in readings_with_max_temp]
        min_temps = [reading.min_temp for reading in readings_with_min_temp]
        mean_humidities = [reading.mean_humidity for reading in readings_with_humidity]

        return ReportResult(
            highest=sum(max_temps) / len(max_temps),
            lowest=sum(min_temps) / len(min_temps),
            humidity=sum(mean_humidities) / len(mean_humidities),
        )

    def filter_readings(self, readings, humidity_field):
        readings_with_max_temp = self.filter_valid(readings, "max_temp")
        readings_with_min_temp = self.filter_valid(readings, "min_temp")
        readings_with_humidity = self.filter_valid(readings, humidity_field)

        if not readings_with_max_temp or not readings_with_min_temp or not readings_with_humidity:
            return None

        return readings_with_max_temp, readings_with_min_temp, readings_with_humidity

    def filter_valid(self, readings, field_name):
        return [reading for reading in readings if getattr(reading, field_name) is not None]
