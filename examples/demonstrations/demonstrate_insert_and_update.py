from datetime import datetime

from UofG_PP.models import IV, Wafer, Die, IVModelReadings

# First up# Uncomment the following two lines if you need to clean up the database before running this script.
# clear_database()
# upload_all()

# 1. insert()

# Insert a new model instance into the database

iv = IV(wafer='aaa', die='abb', comment='HEY', institution='BEY', author='BAE',
    date=datetime(year=2010, month=11, day=10), voltageStep=3.9, stepDelay=4.2, stepMeasurement=4,
    compliance=2.23, readings=[IVModelReadings(time=3, voltage=2.0, currentAverage=3.9, currentStdev=4.2, temperature=2.3, humidity=6.9)])

iv.insert()

# 2. Update

# After getting a model instance from the database and changing it locally, update the changes so they
# are reflected in the database

tariq_iv = IV.find_one(author="Danial Tariq")
tariq_iv.author = "Not Danial Tariq"
tariq_iv.update()

# Example
# If we wanted to rename a wafer from iLGAD_3374-16 to 3374-16

# First, change the wafer
wafer = Wafer.find_one(name='iLGAD_3374-16')
wafer.name = '3374-16'

# Now change the dies
dies = Die.find(wafer='iLGAD_3374-16')
for die in dies:
    die.wafer = '3374-16'
    die.update()



# 3. insert_or_update

# When called on an instance of a model updates it inside the database,
# however if it is a new model instance, it will insert i

# like update
iv = IV.find_one(institution="University of Glasgow")
iv.institution = "University of Paris"
iv.insert_or_update()

# like insert
die = Die(wafer='', name='a', anode_type='anode', device_type='device', size=2.12, pitch=3.13,
                   n_channels=2.1111334)
die.insert_or_update()
