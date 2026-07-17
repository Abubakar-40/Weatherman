from datetime import date

from weather.constants import BLUE, RED, RESET


class WeatherReport:
    def generate_yearly_summary(self, result):
        highest_date = result.highest_date.strftime("%B %d")
        highest_line = f"Highest: {int(result.highest):02d}C on {highest_date}"

        lowest_date = result.lowest_date.strftime("%B %d")
        lowest_line = f"Lowest: {int(result.lowest):02d}C on {lowest_date}"

        humidity_date = result.humidity_date.strftime("%B %d")
        humidity_line = f"Humidity: {int(result.humidity)}% on {humidity_date}"

        report_text = "\n".join([highest_line, lowest_line, humidity_line])

        return report_text

    def generate_monthly_average(self, result):
        highest_line = f"Highest Average: {round(result.highest)}C"
        lowest_line = f"Lowest Average: {round(result.lowest)}C"
        humidity_line = f"Average Mean Humidity: {round(result.humidity)}%"
        report_text = "\n".join([highest_line, lowest_line, humidity_line])

        return report_text

class ChartReport:
    def prepare(self, readings, year, month):
        sorted_readings = sorted(readings, key=lambda reading: reading.date)

        if not sorted_readings:
            return None

        month_heading = date(year, month, 1).strftime("%B %Y")

        return sorted_readings, month_heading

    def generate_daily(self, readings, year, month):
        prepared = self.prepare(readings, year, month)

        if prepared is None:
            return None

        sorted_readings, month_heading = prepared
        lines = [month_heading]

        for reading in sorted_readings:
            day_number = reading.date.strftime("%d")

            if reading.max_temp is not None:
                temperature_value = int(round(reading.max_temp))
                bar = "+" * temperature_value
                lines.append(f"{day_number} {RED}{bar}{RESET} {temperature_value:02d}C")

            if reading.min_temp is not None:
                temperature_value = int(round(reading.min_temp))
                bar = "+" * temperature_value
                lines.append(f"{day_number} {BLUE}{bar}{RESET} {temperature_value:02d}C")

        report_text = "\n".join(lines)

        return report_text

    def generate_combined(self, readings, year, month):
        prepared = self.prepare(readings, year, month)

        if prepared is None:
            return None

        sorted_readings, month_heading = prepared
        lines = [month_heading]

        for reading in sorted_readings:
            if reading.max_temp is None or reading.min_temp is None:
                continue

            day_number = reading.date.strftime("%d")
            low_value = int(round(reading.min_temp))
            high_value = int(round(reading.max_temp))
            bar = f"{BLUE}{'+' * low_value}{RED}{'+' * high_value}{RESET}"
            lines.append(f"{day_number} {bar} {low_value:02d}C - {high_value:02d}C")

        report_text = "\n".join(lines)

        return report_text
