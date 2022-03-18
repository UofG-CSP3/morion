from morion import download_one, download_many
from UofG_PP.models import IV, Wafer, Die
from demonstration_Feb import clear_database, upload_all


# Uncomment the following two lines if you need to clean up the database before running this script.
# clear_database()
# upload_all()

# 1. Download a single document.

# Download a single IV file which matches the criteria into a file called 'test_download.txt'
download_one(IV, 'test_download.txt', author='Dima Maneuski')

# If no file name is specified, the id of the document will be used.
download_one(Wafer, name='iLGAD_3374-15')

# You can format the file name yourself, using python format strings.
# The following will download a iLGAD die, and the name of the file will be
# the wafer, the die name, and the anode type of the downloaded die.
download_one(Die, "{wafer}_{name}_{anode_type}.txt", device_type='iLGAD')

# In the above line, the fields in the format string need to match the fields for Die (defined in UofG_PP/models.py)


# 2. Downloading multiple documents

# Download multiple documents which match the criteria, into a folder called 'downloaded_dies'
# Like before, we can format the file name as well.
download_many(Die, directory='downloaded_dies/', filepath="{wafer}_{name}.txt", anode_type="pixels")

# You can further group downloaded documents using the 'group' parameter.
# The following line of code will download all IVs performed by the University of Glasgow.
# It will download them into downloaded_ivs directory.
# The folder will be further subdivided into subdirectories, corresponding to the wafer, and the author.
download_many(IV, directory='downloaded_ivs/', filepath='IV_{wafer}_{die}.txt', group=['wafer', 'author'], institution='University of Glasgow')
