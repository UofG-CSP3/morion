from morion.filewriter import register_writer
from .standard_writers import standard_experiment_write, standard_component_write
from .models import IV, Wafer, Die
from pathlib import Path


def get_header(header_name: str):
    filepath: Path = Path(__file__).parent / 'headers' / header_name
    return str(filepath)


@register_writer(model=IV, use_when=lambda _: True)
def iv_writer(filepath: str, model: IV):
    header = get_header("IV_header.csv")
    standard_experiment_write(model=model,new_file=filepath,header_filepath=header, defaults={'measurementType': 'IV'})


@register_writer(model=Wafer, use_when=lambda _: True)
def wafer_writer(filepath: str, model: Wafer):
    header = get_header('Wafer_header.csv')
    standard_component_write(model=model, new_file=filepath, header_filepath=header, defaults={'Component': 'Wafer'})


@register_writer(model=Die, use_when=lambda _:True)
def die_writer(filepath: str, model: Die):
    header = get_header('Die_header.csv')
    standard_component_write(model=model, new_file=filepath, header_filepath=header, defaults={'Component': 'Die'})
