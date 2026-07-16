import argparse

from weather.calculators import Calculator
from weather.reports import ChartReport, WeatherReport


def parse_year_month(value):
    year_text, month_text = value.split("/")
    year = int(year_text)
    month = int(month_text)

    if month < 1 or month > 12:
        raise argparse.ArgumentTypeError(f"invalid month: {month}")

    return year, month

def build_argument_parser():
    argument_parser = argparse.ArgumentParser(
        prog="weatherman",
        description="Generate weather reports from historical weather data files.",
    )
    argument_parser.add_argument(
        "data_dir",
        help="Path to the directory containing weather data files.",
    )
    argument_parser.add_argument(
        "-e",
        metavar="YYYY",
        type=int,
        help="Print the yearly summary report for the given year, e.g. -e 2011.",
    )
    argument_parser.add_argument(
        "-a",
        metavar="YYYY/M",
        type=parse_year_month,
        help="Print the monthly averages report for the given year and month, e.g. -a 2005/6.",
    )
    argument_parser.add_argument(
        "-c",
        metavar="YYYY/MM",
        type=parse_year_month,
        help="Print the daily temperature chart for the given year and month, e.g. -c 2011/03.",
    )
    argument_parser.add_argument(
        "-b",
        metavar="YYYY/M",
        type=parse_year_month,
        help="Print the combined daily bar chart for the given year and month, e.g. -b 2011/3.",
    )

    return argument_parser

def exit_with_error(message):
    raise SystemExit(f"Error: {message}")

def run_yearly_summary_report(data_parser, year):
    readings = data_parser.get_readings_for_year(year)
    result = Calculator().calculate_yearly_summary(readings)

    if result is None:
        exit_with_error("Not enough weather data available for the requested year.")

    report_text = WeatherReport().generate_yearly_summary(result)
    print(report_text,"\n")

def run_monthly_average_report(data_parser, year, month):
    readings = data_parser.get_readings_for_month(year, month)
    result = Calculator().calculate_monthly_average(readings)

    if result is None:
        exit_with_error("Not enough weather data available for the requested month.")

    report_text = WeatherReport().generate_monthly_average(result)
    print(report_text,"\n")

def run_daily_chart_report(data_parser, year, month):
    readings = data_parser.get_readings_for_month(year, month)
    report_text = ChartReport().generate_daily(readings, year, month)

    if report_text is None:
        exit_with_error("Not enough weather data available for the requested month.")

    print(report_text,"\n")

def run_combined_chart_report(data_parser, year, month):
    readings = data_parser.get_readings_for_month(year, month)
    report_text = ChartReport().generate_combined(readings, year, month)

    if report_text is None:
        exit_with_error("Not enough weather data available for the requested month.")

    print(report_text,"\n")
