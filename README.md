# Weatherman

A command-line application that reads historical weather data files and
generates weather reports based on the requested options.

## Setup

1. Create and activate a virtual environment:

   ```bash
   python -m venv .venv
   source .venv/bin/activate
   ```

2. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

3. Download the weather data files and place them in a folder, e.g.
   `weather_files/`:

   https://drive.google.com/file/d/1nu_ufYsrrXZfcPColXSpPYJB7-xIpkE2/view

## Usage

```bash
python main.py --help
```

```
usage: weatherman [-h] [-e YYYY] [-a YYYY/M] [-c YYYY/MM] data_dir

Generate weather reports from historical weather data files.

positional arguments:
  data_dir    Path to the directory containing weather data files.

options:
  -h, --help  show this help message and exit
  -e YYYY     Print the yearly summary report for the given year, e.g. -e
              2011.
  -a YYYY/M   Print the monthly averages report for the given year and month,
              e.g. -a 2005/6.
  -c YYYY/MM  Print the daily temperature chart for the given year and month,
              e.g. -c 2011/03.
  -b YYYY/M   Print the combined daily bar chart for the given year and month,
              e.g. -b 2011/3.
```

## What's implemented

### Yearly Summary Report (`-e YYYY`)

Prints the highest temperature, lowest temperature, and most humid day for
the given year, along with the day each occurred.

```bash
python main.py weather_files -e 2007
```

```
Highest: 44C on November 04
Lowest: -1C on February 22
Humidity: 100% on February 11
```

### Monthly Averages Report (`-a YYYY/M`)

Prints the average of the daily highs, average of the daily lows, and
average mean humidity for the given year and month.

```bash
python main.py weather_files -a 2010/12
```

```
Highest Average: 12C
Lowest Average: 5C
Average Mean Humidity: 44%
```

### Daily Temperature Chart (`-c YYYY/MM`)

Prints two horizontal bar charts per day for the given month — the day's
high temperature (in red) and low temperature (in blue). Colors show when
run in an actual terminal; shown below without color codes.

```bash
python main.py weather_files -c 2011/03
```

```
March 2011
01 +++++ 05C
01  00C
02 ++++ 04C
02  00C
03 ++++++ 06C
```

### Combining multiple reports

Flags can be combined in a single run.

```bash
python main.py weather_files -e 2007 -a 2010/12
```

```
Highest: 44C on November 04
Lowest: -1C on February 22
Humidity: 100% on February 11

Highest Average: 12C
Lowest Average: 5C
Average Mean Humidity: 44%
```

### Combined Daily Bar Chart (`-b YYYY/M`) — bonus

Prints one bar per day, combining the low and high temperatures into a
single bar (bar length = low + high), labeled as `LOWC - HIGHC` at the end.
Colors show when run in an actual terminal; shown below without color codes.

```bash
python main.py weather_files -b 2011/3
```

```
March 2011
01 +++++ 00C - 05C
02 ++++ 00C - 04C
03 ++++++ 00C - 06C
04 ++++ 00C - 04C
05 +++++++++ 03C - 06C
```

## Project structure

```
weatherman/
├── main.py               # Entry point: only calls into utils.py
├── utils.py              # CLI argument parsing and report orchestration
├── requirements.txt
└── weather/
    ├── classes.py         # WeatherRecord and Reports data structures
    ├── services.py        # Reads weather files and computes report results
    ├── constants.py       # ANSI color codes used by the chart reports
    └── reports.py         # Formats calculation results into printable text
```

The flow for every report follows the same pipeline:

```
services (reads files, computes results) -> report (formats text)
```

All report types from the spec (`-e`, `-a`, `-c`, `-b`) are implemented.
