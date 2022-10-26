import csv
import os
import io


def write_csv_lines(test_data, write_headers=True):
    # Write your test data in a temporary file
    tmp_file = r"test.csv"
    fieldnames = ["voornaam", "achternaam", "email"]
    with open(tmp_file, "w") as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        if write_headers:
            writer.writeheader()
        for row in test_data:
            writer.writerow(row)
    return open("test.csv", "r")
