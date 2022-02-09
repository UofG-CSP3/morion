import csv


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

        # Parse the values in the header of the experiment.
        for header_row, experiment_row in zip(header_reader, experiment_reader):
            experiment_dict.update(dict(zip(header_row, experiment_row)))

        # Now parse in the readings
        fields = {index: field for index, field in enumerate(next(experiment_reader))}
        readings = [{fields[i]: float(val) for i, val in enumerate(line)} for line in experiment_reader]
        experiment_dict['readings'] = readings

    return experiment_dict
