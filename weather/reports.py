from datetime import date

from weather.models import MonthlyAverages, WeatherReading, YearlySummary


RED = "\033[31m"
BLUE = "\033[34m"
RESET = "\033[0m"


class YearlySummaryReport:
    def generate(self, summary: YearlySummary):
        highest_line = self.format_temperature_line(
            "Highest",
            summary.highest_temp,
            summary.highest_temp_date,
        )
        lowest_line = self.format_temperature_line(
            "Lowest",
            summary.lowest_temp,
            summary.lowest_temp_date,
        )
        humidity_line = self.format_humidity_line(
            summary.most_humid_day_humidity,
            summary.most_humid_day_date,
        )
        report_text = "\n".join([highest_line, lowest_line, humidity_line])

        return report_text

    def format_temperature_line(self, label, temperature, reading_date):
        formatted_date = reading_date.strftime("%B %d")
        line = f"{label}: {int(temperature):02d}C on {formatted_date}"

        return line

    def format_humidity_line(self, humidity, reading_date):
        formatted_date = reading_date.strftime("%B %d")
        line = f"Humidity: {int(humidity)}% on {formatted_date}"

        return line


class MonthlyAverageReport:
    def generate(self, averages: MonthlyAverages):
        highest_line = f"Highest Average: {round(averages.avg_highest_temp)}C"
        lowest_line = f"Lowest Average: {round(averages.avg_lowest_temp)}C"
        humidity_line = f"Average Mean Humidity: {round(averages.avg_mean_humidity)}%"
        report_text = "\n".join([highest_line, lowest_line, humidity_line])

        return report_text


class DailyChartReport:
    def generate(self, readings: list[WeatherReading], year: int, month: int):
        sorted_readings = sorted(readings, key=lambda reading: reading.reading_date)

        if not sorted_readings:
            return None

        month_heading = date(year, month, 1).strftime("%B %Y")
        lines = [month_heading]

        for reading in sorted_readings:
            day_number = reading.reading_date.strftime("%d")

            if reading.max_temp is not None:
                lines.append(self.format_bar_line(day_number, reading.max_temp, RED))

            if reading.min_temp is not None:
                lines.append(self.format_bar_line(day_number, reading.min_temp, BLUE))

        report_text = "\n".join(lines)

        return report_text

    def format_bar_line(self, day_number, temperature, color):
        temperature_value = int(round(temperature))
        bar = "+" * temperature_value
        line = f"{day_number} {color}{bar}{RESET} {temperature_value:02d}C"

        return line


class CombinedChartReport:
    def generate(self, readings: list[WeatherReading], year: int, month: int):
        sorted_readings = sorted(readings, key=lambda reading: reading.reading_date)

        if not sorted_readings:
            return None

        month_heading = date(year, month, 1).strftime("%B %Y")
        lines = [month_heading]

        for reading in sorted_readings:
            if reading.max_temp is None or reading.min_temp is None:
                continue

            day_number = reading.reading_date.strftime("%d")
            lines.append(self.format_bar_line(day_number, reading.min_temp, reading.max_temp))

        report_text = "\n".join(lines)

        return report_text

    def format_bar_line(self, day_number, low_temp, high_temp):
        low_value = int(round(low_temp))
        high_value = int(round(high_temp))
        bar = f"{BLUE}{'+' * low_value}{RED}{'+' * high_value}{RESET}"
        line = f"{day_number} {bar} {low_value:02d}C - {high_value:02d}C"

        return line
