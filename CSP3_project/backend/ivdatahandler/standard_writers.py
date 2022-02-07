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
