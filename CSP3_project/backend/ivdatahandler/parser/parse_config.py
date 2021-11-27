from pathlib import Path
import csv

# TODO: make this more generic
HEADER_PATH = Path(__file__).with_name('experiment_header.csv')


def read_header(filepath: str = HEADER_PATH) -> list:
    with open(filepath, 'r') as f:
        reader = csv.reader(f)
        return list(reader)
