import csv

from .mongomodel import MongoModel

#TODO for optional fields, where do we put them in the new file. Need to ask Dima...

def standard_experiment_write(
        model: MongoModel,
        new_file: str,
        header_filepath,
        defaults = {},
        experiment_delim='\t',
        header_delim: str = ','
):
    defaults.update(model.dict(by_alias=True))
    model_dict = defaults
    del model_dict['_id']



    with open(new_file, 'w', newline='') as experiment_file, open(header_filepath, 'r') as header_f:
        header_reader = csv.reader(header_f, delimiter=header_delim)
        experiment_writer = csv.writer(experiment_file, delimiter=experiment_delim)
        
        for row in header_reader:
            write_row = [model_dict[cell] for cell in row]
            experiment_writer.writerow(write_row)
        
        readings_list: list[dict] = model_dict['readings']
        fields = []
        for reading_dict in readings_list:
            fields.extend([key for key in reading_dict if key not in fields])

        experiment_writer.writerow(fields)

        for reading in readings_list:
            row = [reading.get(field, '') for field in fields]
            experiment_writer.writerow(row)


        #TODO specify number of digits for floating numbers

def standard_component_write(
        model: MongoModel,
        new_file: str,
        header_filepath,
        defaults=None,
        component_delim='\t',
        header_delim: str = ','
):
    if defaults is None:
        defaults = {}

    defaults.update(model.dict(by_alias=True))
    model_dict = defaults
    del model_dict['_id']

    with open(new_file, 'w', newline='') as component_file, open(header_filepath, 'r') as header_f:
        header_reader = csv.reader(header_f, delimiter=header_delim)
        component_writer = csv.writer(component_file, delimiter=component_delim)

        header_fields = set()
        for row in header_reader:
            header_fields.update(row)
            write_row = [model_dict[cell] for cell in row]
            component_writer.writerow(write_row)

        component_info = {field: value for field, value in model_dict.items() if field not in header_fields}
        component_file.write('\n')

        for field, value in component_info.items():
            value = value if value else ''
            component_file.write(f'{field}{component_delim}{value}\n')
