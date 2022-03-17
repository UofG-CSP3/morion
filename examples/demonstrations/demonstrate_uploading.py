from morion import upload_file, upload_bulk, upload_directory
from demonstration_Feb import clear_database


clear_database()

# 1. Upload a single file
upload_file('ivs/IV_wafer_iLGAD_3374-15_die_0_0.txt')
upload_file('wafers/Wafer_iLGAD_3374-15.txt')

# If a document with the same if already exists in the database, set 'upsert' to True to replace it.
# If upsert is False, the following line would crash as we've already uploaded this file above.
upload_file('wafers/Wafer_iLGAD_3374-15.txt', upsert=True)

# 2. Uploading multiple files at a time
upload_bulk(
    ['ivs/IV_wafer_iLGAD_3374-16_die_0_1.txt', 'dies/Die_iLGAD_3374-16_0_1.txt', 'wafers/Wafer_iLGAD_3374-16.txt'])

# 3. Uploading a directory

# Upload the entire wafers directory at once.
upload_directory('wafers/', upsert=True)

# Can also use patterns to upload only specific files in a directory.
# For example, only upload dies between 0_0 and 0_3
upload_directory('dies/', pattern='*0_[0-3]*.txt')
