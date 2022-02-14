import csv
import random

from pathlib import Path
import datetime

# This is probably wrong as the device type should probably be part of the die, not the wafer.
# Need to ask Dima for clarification.
wafers = ['iLGAD_3374-15', 'iLGAD_3374-16', 'iLGAD_3374-16', 'iLGAD_3374-17', 'iLGAD_3374-18']
die_row = 4
die_col = 4


def create_iv_file(wafer, die):
    author = random.choice(['Dima Maneuski', 'Danial Tariq', 'James McClure', 'Ciara Losel', 'Franciszek Sowul',
                            'Eren Oezveren'])

    with open(f'../../CSP3_project/ivs/IV_wafer_{wafer}_die_{die}.txt', 'w', newline='') as f:
        writer = csv.writer(f, delimiter='\t')
        writer.writerow([wafer, die, 'IV'])
        writer.writerow(['comment'])
        writer.writerow(['University of Glasgow', author, datetime.datetime.now()])
        writer.writerow([random.randint(0, 5) for i in range(3)] + [random.random()])
        writer.writerow(['t/s','U/V','Iavg/uA','Istd/uA','T/C','RH/%'])
        time = random.randint(0,5)
        for i in range(100):
            writer.writerow([time] + ["%.2f" % random.random() for i in range(5)])
            time += random.randint(1,10)


def create_die_file(wafer, name):
    anode_type = random.choice(['pad', 'pixels', 'strips', 'other'])
    device_type = wafer.split('_')[0]

    with open(f'../../CSP3_project/dies/Die_{wafer}_{name}.txt', 'w', newline='') as f:
        writer = csv.writer(f, delimiter='\t')
        writer.writerow(['Die', wafer, name])
        writer.writerow([anode_type, device_type, random.randint(0, 5)])
        writer.writerow([])
        writer.writerow(['pitch', "%.2f" % random.random()])
        writer.writerow(['n_channels', random.randint(0, 5)])


def create_die_and_iv_files():
    Path('../../CSP3_project/dies').mkdir(exist_ok=True)
    Path('../../CSP3_project/ivs').mkdir(exist_ok=True)

    for wafer in wafers:
        for row in range(die_row):
            for col in range(die_col):
                name = f'{row}_{col}'
                create_die_file(wafer, name)
                create_iv_file(wafer, name)

'''
    mean_depletion_voltage: float
    depletion_voltage_stdev: float
    thickness: float
    handle_wafer: str
    sheet_resistance: float
'''
def create_wafer_file(wafer):
    material_types = ['Material 1', 'Meterial 2', 'Material 3']
    mask_designs = ['Design 1', 'Design 2', 'Design 3']
    production_date = datetime.datetime.now()
    production_run_data = 'www.example.com'

    with open(f'../../CSP3_project/wafers/Wafer_{wafer}.txt', 'w', newline='') as f:
        writer = csv.writer(f, delimiter='\t')
        writer.writerow(['Wafer', wafer])
        writer.writerow([random.choice(material_types), random.choice(mask_designs), production_date])
        writer.writerow([production_run_data])
        writer.writerow([])
        writer.writerow(['handle_wafer', 'Handle'])
        for i in ['oxide_thickness', 'mean_depletion_voltage', 'depletion_voltage_stdev', 'thickness', 'sheet_resistance']:
            writer.writerow([i, "%.2f" % random.random()])


def create_wafer_files():
    Path('../../CSP3_project/wafers').mkdir(exist_ok=True)

    for wafer in wafers:
        create_wafer_file(wafer)


def main():
    create_die_and_iv_files()
    create_wafer_files()


if __name__ == '__main__':
    main()
