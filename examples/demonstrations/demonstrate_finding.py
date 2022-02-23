from backend.ivdatahandler import download_one, download_many
from backend.models import IV, Wafer, Die
from demonstration_Feb import clear_database, upload_all

# 1. First upload a test file (see demonstrate_uploading.py) to test, in this case just upload one file

# 2. Analyze the find_one method.

# With the uploaded file, lets see if we can find it in the database

find_one("IV_wafer_iLGAD_3374-15_die_0_0.txt")

# Let's say we want to check certain details in this file. Say we also just want one example
# of this, we can check the following things for:

# Author:

find_one("IV_wafer_iLGAD_3374-15_die_0_0.txt", author="Dima Maneuski")

# Institution:

find_one("IV_wafer_iLGAD_3374-15_die_0_0.txt", institution="University of Glasgow")

# One can query and find any of the defined fields, whether they are mandatory fields apart of the
# mongomodels or if they are custom fields.

# 2. Analyze the find method.

# This method can be used to examine all the entries in the database of the queried type

find("IV_wafer_iLGAD_3374-15_die_0_0.txt", institution="University of Glasgow")

