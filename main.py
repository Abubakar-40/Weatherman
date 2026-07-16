import argparse
import sys
from pathlib import Path

from weather.calculators import YearlySummaryCalculator
from weather.parser import WeatherDataParser
from weather.reports import YearlySummaryReport


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

    return argument_parser

def run_yearly_summary_report(data_parser: WeatherDataParser, year: int):
    readings = data_parser.get_readings_for_year(year)
    summary = YearlySummaryCalculator().calculate(readings)
    report_text = YearlySummaryReport().generate(summary)
    print(report_text)

def main():
    argument_parser = build_argument_parser()
    arguments = argument_parser.parse_args()
    data_parser = WeatherDataParser(Path(arguments.data_dir))

    try:
        if arguments.e is not None:
            run_yearly_summary_report(data_parser, arguments.e)
    except ValueError as error:
        print(f"Error: {error}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()