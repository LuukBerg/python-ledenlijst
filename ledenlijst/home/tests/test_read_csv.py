from django.test import TestCase
from home.views import read_members_from_csv_file
import csv
from home.tests.csv_test_util import write_csv_lines

# Create your tests here.


class ReadCSVFileTestCase(TestCase):
    def test_read_csv_file_without_header(self):
        rows = [
            {
                "voornaam": "test voornaam",
                "achternaam": "test achternaam",
                "email": "testemail@email.nl",
            }
        ]
        file = write_csv_lines(rows)
        members = read_members_from_csv_file(file)
        self.assertTrue(len(members), 1)
        self.assertTrue(members[0].email, "testemail@email.nl")
        self.assertTrue(members[0].firstname, "test voornaam")
        self.assertTrue(members[0].lastname, "test achternaam")

    def test_read_csv_file_with_header(self):
        rows = [
            {
                "voornaam": "test voornaam",
                "achternaam": "test achternaam",
                "email": "testemail@email.nl",
            }
        ]
        file = write_csv_lines(rows, False)
        members = read_members_from_csv_file(file)
        self.assertTrue(len(members), 1)
        self.assertTrue(members[0].email, "testemail@email.nl")
        self.assertTrue(members[0].firstname, "test voornaam")
        self.assertTrue(members[0].lastname, "test achternaam")
