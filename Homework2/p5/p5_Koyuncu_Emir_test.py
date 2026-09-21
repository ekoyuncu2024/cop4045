"""Unit tests for the weather-station observation program."""

import csv
import os
import tempfile
import unittest

from p5_Koyuncu_Emir import (read_observations, station_outliers,
                             station_statistics, write_statistics)


class WeatherStationTest(unittest.TestCase):
    """Tests observation validation, calculations, and file output."""

    def make_input_file(self, contents):
        """Creates an input file that is removed after the current test."""
        temporary_file = tempfile.NamedTemporaryFile(
            mode="w", encoding="utf-8", newline="", delete=False)
        temporary_file.write(contents)
        temporary_file.close()
        self.addCleanup(self.remove_file, temporary_file.name)
        return temporary_file.name

    def remove_file(self, filename):
        """Removes a temporary file if it still exists."""
        if os.path.exists(filename):
            os.remove(filename)

    def test_reads_several_stations_and_sorts_dates(self):
        filename = self.make_input_file(
            "North,09:30:00 AM 04/21/2026,12.5\n"
            "South,08:00:00 AM 04/20/2026,-8.0\n"
            "North,09:28:09 AM 04/20/2026,-2.5\n")

        observations, errors = read_observations(filename)

        self.assertEqual(errors, [])
        self.assertEqual(observations["North"], [
            ("09:28:09 AM 04/20/2026", -2.5),
            ("09:30:00 AM 04/21/2026", 12.5),
        ])
        self.assertEqual(observations["South"], [
            ("08:00:00 AM 04/20/2026", -8.0),
        ])

    def test_rejects_malformed_lines(self):
        filename = self.make_input_file(
            "only,two\n"
            "Station,not a date,10\n"
            ",09:28:09 AM 04/20/2026,10\n")

        observations, errors = read_observations(filename)

        self.assertEqual(observations, {})
        self.assertEqual([number for number, message in errors], [1, 2, 3])

    def test_rejects_duplicate_observations(self):
        filename = self.make_input_file(
            "A,09:28:09 AM 04/20/2026,10\n"
            "A,09:28:09 AM 04/20/2026,11\n")

        observations, errors = read_observations(filename)

        self.assertEqual(observations["A"], [
            ("09:28:09 AM 04/20/2026", 10.0),
        ])
        self.assertEqual(errors[0][0], 2)
        self.assertIn("duplicate", errors[0][1])

    def test_rejects_invalid_temperature_ranges(self):
        filename = self.make_input_file(
            "A,09:28:09 AM 04/20/2026,-100.1\n"
            "B,09:28:09 AM 04/20/2026,150.1\n"
            "C,09:28:09 AM 04/20/2026,not-a-number\n")

        observations, errors = read_observations(filename)

        self.assertEqual(observations, {})
        self.assertEqual(len(errors), 3)

    def test_accepts_boundary_temperatures(self):
        filename = self.make_input_file(
            "A,09:28:09 AM 04/20/2026,-100.0\n"
            "B,09:28:09 AM 04/20/2026,150.0\n")

        observations, errors = read_observations(filename)

        self.assertEqual(errors, [])
        self.assertEqual(observations["A"][0][1], -100.0)
        self.assertEqual(observations["B"][0][1], 150.0)

    def test_calculates_station_statistics(self):
        observations = {
            "A": [("first", -5.0), ("second", 10.0), ("third", 25.0)],
            "B": [("only", 7.5)],
        }

        statistics = station_statistics(observations)

        self.assertEqual(statistics["A"], (-5.0, 25.0, 10.0))
        self.assertEqual(statistics["B"], (7.5, 7.5, 7.5))

    def test_finds_latest_temperature_outliers(self):
        observations = {
            "A": [("first", 0.0), ("latest", 10.0)],
            "B": [("first", 10.0), ("latest", 0.0)],
        }

        self.assertEqual(
            station_outliers(observations),
            {"A": ("latest", 10.0, 5.0)})

    def test_writes_sorted_statistics_with_one_decimal(self):
        output_file = tempfile.NamedTemporaryFile(delete=False)
        output_file.close()
        self.addCleanup(self.remove_file, output_file.name)
        statistics = {
            "Zulu": (1.0, 2.0, 1.5),
            "Alpha": (-2.0, 3.0, 0.25),
        }

        write_statistics(output_file.name, statistics)

        with open(output_file.name, "r", encoding="utf-8", newline="") as file:
            rows = list(csv.reader(file))
        self.assertEqual(rows, [
            ["station", "minimum", "maximum", "mean"],
            ["Alpha", "-2.0", "3.0", "0.2"],
            ["Zulu", "1.0", "2.0", "1.5"],
        ])

    def test_missing_input_file(self):
        missing_filename = os.path.join(
            tempfile.gettempdir(), "missing_weather_observations_12345.csv")
        self.remove_file(missing_filename)

        with self.assertRaises(FileNotFoundError):
            read_observations(missing_filename)


if __name__ == "__main__":
    unittest.main()
