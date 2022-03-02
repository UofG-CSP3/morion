from backend.ivdatahandler import download_one, download_many
from backend.models import IV, Wafer, Die
from demonstration_Feb import clear_database, upload_all

# 1. First upload a test file (see demonstrate_uploading.py) to test, in this case just upload one file

# 2. delete_one

# This method will delete one instance of this model from a given database,
# it will delete one random entry

delete_one("IV_wafer_iLGAD_3374-15_die_0_0.txt", author="Steve Stevey")

# 3. delete_many

# THis method like the above method will delete entries in the database, but will delete all entries
# in a given database

delete_many("IV_wafer_iLGAD_3374-15_die_0_0.txt", author="Steve Stevey")

# 4 find_one_and_delete

# This method will find and delete an instance in a database

find_one_and_delete("IV_wafer_iLGAD_3374-15_die_0_0.txt", Institution="University of Edinburgh")

# 5. delete

# THis method will delete an entry of the database, like a die or iv

iv = IV.find_one()
iv.delete()
