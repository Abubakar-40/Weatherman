from dataclasses import dataclass
from datetime import date


@dataclass
class WeatherReading:
    date: date
    max_temp: float | None
    min_temp: float | None
    max_humidity: float | None
    mean_humidity: float | None


@dataclass
class ReportResult:
    highest: float
    lowest: float
    humidity: float
    highest_date: date | None = None
    lowest_date: date | None = None
    humidity_date: date | None = None
