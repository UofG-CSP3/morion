import csv


def parse_header(header_reader: csv.reader, file_reader: csv.reader) -> dict:
    d = {}
    for header_row, file_row in zip(header_reader, file_reader):
        d.update(dict(zip(header_row, file_row)))
    return d


def standard_experiment(
        header_filepath: str,
        experiment_filepath: str,
        header_delim: str = ',',
        experiment_delim: str = '\t'
):
    """
    Standard reader for experiment files. Takes in an experiment data file and header template file and parses its contents into a dictionary.
    """
    experiment_dict = {}

    with open(header_filepath) as header_f, open(experiment_filepath) as experiment_f:
        header_reader = csv.reader(header_f, delimiter=header_delim)
        experiment_reader = csv.reader(experiment_f, delimiter=experiment_delim)

        experiment_dict.update(parse_header(header_reader, experiment_reader))

        # Now parse in the readings
        fields = {index: field for index, field in enumerate(next(experiment_reader))}
        readings = [{fields[i]: val if val != '' else None for i, val in enumerate(line)} for line in experiment_reader]
        experiment_dict['readings'] = readings

    return experiment_dict


def standard_component(
        header_filepath: str,
        component_filepath: str,
        header_delim: str = ',',
        component_delim: str = '\t'
):
    component_dict = {}
    with open(header_filepath) as header_f, open(component_filepath) as experiment_f:
        header_reader = csv.reader(header_f, delimiter=header_delim)
        component_reader = csv.reader(experiment_f, delimiter=component_delim)

        component_dict.update(parse_header(header_reader, component_reader))
        for row in component_reader:
            if len(row) == 0:
                continue

            key, *value = row
            component_dict[key] = ''.join(value)
    return component_dict
