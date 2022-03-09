from morion import find_one, find, find_one_and_delete, find_one_and_replace
from CSP3_project.models import IV, Wafer, Die
from demonstration_February import clear_database, upload_all

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

# 3. Analyze the find_one_and_delete method.

# This method can be used to find a given entry in the database and delete it.
# It will delete only one instance

find_one_and_delete("IV_wafer_iLGAD_3374-15_die_0_0.txt", author="John Johnson")

# 4. Analyze the find_one_replace method.

# This method can be used to find a given entry in the database and delete it.
# It will delete only one instance

find_one_and_replace("IV_wafer_iLGAD_3374-15_die_0_0.txt", comment="I love steak")