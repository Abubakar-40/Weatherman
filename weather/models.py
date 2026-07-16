from dataclasses import dataclass
from datetime import date


@dataclass(frozen=True)
class WeatherReading:
    reading_date: date
    max_temp: float | None
    min_temp: float | None
    max_humidity: float | None
    mean_humidity: float | None

@dataclass(frozen=True)
class YearlySummary:
    highest_temp: float
    highest_temp_date: date
    lowest_temp: float
    lowest_temp_date: date
    most_humid_day_humidity: float
    most_humid_day_date: date

@dataclass(frozen=True)
class MonthlyAverages:
    avg_highest_temp: float
    avg_lowest_temp: float
    avg_mean_humidity: float
