import csv
import json
import unittest
from pathlib import Path

ROOT = Path(__file__).parents[1]
PACKAGE = 'green_power_schedule'

def read_csv(name):
    with (ROOT / 'data' / name).open(encoding='utf-8', newline='') as handle:
        return list(csv.DictReader(handle))

def read_json(name):
    return json.loads((ROOT / 'data' / name).read_text(encoding='utf-8'))

class ContractTests(unittest.TestCase):
    def test_package_name_and_data_directory(self):
        self.assertTrue(PACKAGE)
        self.assertTrue((ROOT / 'data').is_dir())

    def test_power_readings_have_explicit_quality(self):
        rows = read_csv('power_readings.csv')
        self.assertTrue({row['source_quality'] for row in rows} == {'metered', 'estimated'})

    def test_unready_batch_is_not_zero_yield(self):
        rows = read_csv('quality_batches.csv')
        row = next(row for row in rows if row['batch_id'] == 'QB02')
        self.assertTrue(row['status'] == 'not_ready' and row['total_units'] == '0')
