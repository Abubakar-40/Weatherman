import argparse
import sys
from pathlib import Path

from weather.calculators import MonthlyAverageCalculator, YearlySummaryCalculator
from weather.parser import WeatherDataParser
from weather.reports import MonthlyAverageReport, YearlySummaryReport


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

    return argument_parser

def run_yearly_summary_report(data_parser: WeatherDataParser, year: int):
    readings = data_parser.get_readings_for_year(year)
    summary = YearlySummaryCalculator().calculate(readings)
    report_text = YearlySummaryReport().generate(summary)
    print(report_text,"\n")

def run_monthly_average_report(data_parser: WeatherDataParser, year: int, month: int):
    readings = data_parser.get_readings_for_month(year, month)
    averages = MonthlyAverageCalculator().calculate(readings)
    report_text = MonthlyAverageReport().generate(averages)
    print(report_text,"\n")

def main():
    argument_parser = build_argument_parser()
    arguments = argument_parser.parse_args()
    data_parser = WeatherDataParser(Path(arguments.data_dir))

    try:
        if arguments.e is not None:
            run_yearly_summary_report(data_parser, arguments.e)

        if arguments.a is not None:
            year, month = arguments.a
            run_monthly_average_report(data_parser, year, month)
    except ValueError as error:
        print(f"Error: {error}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()