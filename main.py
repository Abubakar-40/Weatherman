from pathlib import Path

from utils import (
    build_argument_parser,
    run_combined_chart_report,
    run_daily_chart_report,
    run_monthly_average_report,
    run_yearly_summary_report,
)
from weather.services import WeatherService


def main():
    argument_parser = build_argument_parser()
    arguments = argument_parser.parse_args()
    data_parser = WeatherService(Path(arguments.data_dir))

    if arguments.e is not None:
        run_yearly_summary_report(data_parser, arguments.e)

    if arguments.a is not None:
        year, month = arguments.a
        run_monthly_average_report(data_parser, year, month)

    if arguments.c is not None:
        year, month = arguments.c
        run_daily_chart_report(data_parser, year, month)

    if arguments.b is not None:
        year, month = arguments.b
        run_combined_chart_report(data_parser, year, month)


if __name__ == "__main__":
    main()
