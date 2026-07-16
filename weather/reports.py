from weather.models import YearlySummary


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