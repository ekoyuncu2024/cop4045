"""Read and summarize weather-station observations."""

import csv
import datetime
import math
import sys


DATE_FORMAT = "%I:%M:%S %p %m/%d/%Y"
MINIMUM_TEMPERATURE = -100.0
MAXIMUM_TEMPERATURE = 150.0


def read_observations(filename):
    """Reads valid observations and reports errors found in the input file.

    Args:
        filename: The name of a comma-separated observations file.

    Returns:
        A tuple containing the observations dictionary and a list of errors.
    """
    observations = {}
    errors = []
    seen = set()

    with open(filename, "r", encoding="utf-8", newline="") as input_file:
        reader = csv.reader(input_file)
        for line_number, row in enumerate(reader, start=1):
            if len(row) != 3:
                errors.append(
                    (line_number, "expected three comma-separated fields"))
                continue

            station = row[0].strip()
            date_text = row[1].strip()
            temperature_text = row[2].strip()

            if not station or not date_text or not temperature_text:
                errors.append((line_number, "a required field is empty"))
                continue

            try:
                date = datetime.datetime.strptime(date_text, DATE_FORMAT)
            except ValueError:
                errors.append((line_number, "invalid date"))
                continue

            try:
                temperature = float(temperature_text)
            except ValueError:
                errors.append((line_number, "temperature is not a number"))
                continue

            if (not math.isfinite(temperature)
                    or temperature < MINIMUM_TEMPERATURE
                    or temperature > MAXIMUM_TEMPERATURE):
                errors.append(
                    (line_number, "temperature is outside the valid range"))
                continue

            observation_key = (station, date)
            if observation_key in seen:
                errors.append((line_number, "duplicate station and date"))
                continue

            seen.add(observation_key)
            observations.setdefault(station, []).append(
                (date_text, temperature, date))

    # Keep the parsed datetime while sorting, then remove it from the result.
    for station in observations:
        observations[station].sort(key=lambda item: item[2])
        observations[station] = [
            (date_text, temperature)
            for date_text, temperature, unused_date in observations[station]
        ]

    return observations, errors


def station_statistics(observations):
    """Returns the minimum, maximum, and mean for every station."""
    statistics = {}

    for station, station_observations in observations.items():
        temperatures = [
            temperature
            for unused_date, temperature in station_observations
        ]
        if temperatures:
            statistics[station] = (
                min(temperatures),
                max(temperatures),
                sum(temperatures) / len(temperatures),
            )

    return statistics


def station_outliers(observations):
    """Returns stations whose latest temperature is above their mean."""
    statistics = station_statistics(observations)

    return {
        station: (
            station_observations[-1][0],
            station_observations[-1][1],
            statistics[station][2],
        )
        for station, station_observations in observations.items()
        if (station_observations
            and station_observations[-1][1] > statistics[station][2])
    }


def write_statistics(filename, statistics):
    """Writes station statistics in lexicographic station order."""
    with open(filename, "w", encoding="utf-8", newline="") as output_file:
        writer = csv.writer(output_file)
        writer.writerow(["station", "minimum", "maximum", "mean"])
        for station in sorted(statistics):
            minimum, maximum, mean = statistics[station]
            writer.writerow([
                station,
                "{:.1f}".format(minimum),
                "{:.1f}".format(maximum),
                "{:.1f}".format(mean),
            ])


def main():
    """Runs the weather-station program using command-line filenames."""
    if len(sys.argv) != 3:
        print("Usage: python p5_Koyuncu_Emir.py input.csv output.csv")
        return

    try:
        observations, errors = read_observations(sys.argv[1])
        statistics = station_statistics(observations)
        outliers = station_outliers(observations)

        print("Statistics:")
        for station in sorted(statistics):
            minimum, maximum, mean = statistics[station]
            print("{}: min={:.1f}, max={:.1f}, mean={:.1f}".format(
                station, minimum, maximum, mean))

        print("Outliers:")
        for station in sorted(outliers):
            date, temperature, mean = outliers[station]
            print("{}: {}, temperature={:.1f}, mean={:.1f}".format(
                station, date, temperature, mean))

        if errors:
            print("Rejected input lines:")
            for line_number, error_message in errors:
                print("Line {}: {}".format(line_number, error_message))

        write_statistics(sys.argv[2], statistics)
    except OSError as error:
        print("Could not access a required file: {}".format(error))


if __name__ == "__main__":
    main()
