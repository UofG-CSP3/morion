from datetime import datetime
from pathlib import Path

from morion.filereader import register_reader
from .reader_templates import standard_experiment, standard_component

from .models import IV, Wafer, Die


def get_header(header_name: str):
    filepath: Path = Path(__file__).parent / 'headers' / header_name
    return str(filepath)


def is_iv_file(filepath: str):
    try:
        with open(filepath, 'r') as f:
            return f.readline().strip().split('\t')[2] == 'IV'

    except (FileNotFoundError, IndexError) as err:
        return False


@register_reader(use_when=is_iv_file)
def iv_reader(filepath: str) -> IV:
    d = standard_experiment(header_filepath=get_header('IV_header.csv'), experiment_filepath=filepath)
    # Don't need the measurement type
    d.pop('measurementType')
    # Convert timestamp str to datetime
    d['date'] = datetime.fromisoformat(d.pop('date'))
    return IV(**d)


def is_wafer(filepath: str):
    try:
        with open(filepath, 'r') as f:
            return f.readline().strip().split('\t')[0] == 'Wafer'
    except (FileNotFoundError, IndexError):
        return False


@register_reader(use_when=is_wafer)
def wafer_reader(filepath: str) -> Wafer:
    d = standard_component(header_filepath=get_header('Wafer_header.csv'), component_filepath=filepath)
    d.pop('Component')
    d['production_date'] = datetime.fromisoformat(d['production_date'])

    return Wafer(**d)



def is_die(filepath: str):
    try:
        with open(filepath, 'r') as f:
            return f.readline().strip().split('\t')[0] == 'Die'
    except (FileNotFoundError, IndexError):
        return False


@register_reader(use_when=is_die)
def die_reader(filepath: str) -> Die:
    d = standard_component(header_filepath=get_header('Die_header.csv'), component_filepath=filepath)
    d.pop('Component')

    return Die(**d)
