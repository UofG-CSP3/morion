from morion import download_one, download_many
from UofG_PP.models import IV, Wafer, Die

# 1. First upload a test file (see demonstrate_uploading.py) to test, in this case just upload one file

# 2. Insert

# Insert a new entry into the database

iv = IV.find_one(institution="University of Paris")
iv.insert(temperature=100)

# 3. Update

iv = IV.find_one(author="John Nhoj")
iv.author = "Nohj John"

#4 insert_or_replace

iv = IV.find_one(institution="University of Paris")
iv.insert_or_replace(temperature=100)