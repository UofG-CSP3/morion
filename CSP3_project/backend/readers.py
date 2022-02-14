from datetime import datetime
from pathlib import Path

from .ivdatahandler.filereader import register_reader
from .ivdatahandler.standard_readers import standard_experiment, standard_component

from .models import IV, Wafer


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
    d.pop('measurementType')  # TODO: Maybe add this functionality to the header file?
    # Convert timestamp str to datetime
    d['date'] = datetime.strptime(d.pop('date'), "%Y-%m-%d_%H:%M")

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
