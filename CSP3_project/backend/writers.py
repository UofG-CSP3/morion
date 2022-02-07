from CSP3_project.backend.ivdatahandler import get_header
from .ivdatahandler.filewriter import register_writer
from .ivdatahandler.standard_writers import standard_experiment_write
from .models import IV

from pathlib import Path


def get_header(header_name: str):
    filepath: Path = Path(__file__).parent / 'headers' / header_name
    return str(filepath)


@register_writer(model=IV, use_when=lambda _: True)
def iv_writer(filepath: str, model: IV):
    header = get_header("IV_header.csv")
    standard_experiment_write(model=model,new_file=filepath,header_filepath=header, defaults={'measurementType': 'IV'})
