from UofG_PP.models import IV, Wafer, Die

# Uncomment the following two lines if you need to clean up the database before running this script.
# clear_database()
# upload_all()

# 1. find_one()

# Get one model of a certain type(IV/Wafer/Die/...) from the database

single_iv = IV.find_one()

# Now this model can be altered and reuploaded

single_iv.author = "Me"
single_iv.update()

# We can query by attributes of the model, for example

# Author:

dimas_iv = IV.find_one(author="Dima Maneuski")

# Institution:

uofg_iv = IV.find_one(institution="University of Glasgow")

# We can query by any of the fields of the model

# 2. find()

# This method can be used to find and return all the entries in the database that conform to the query

glasgow_ivs = IV.find(institution="University of Glasgow")

# 3. find_one_and_delete()

# This method will delete one instance of the Die model that conforms to the query from the database
# and return that instance

Die.find_one_and_delete(size=2.0)

# 4. find_and_replace()

# This method can be called on a model to replace a model in the database that conforms to the query
# Will return the model that has been replaced


uofg_iv.find_and_replace(comment="comment")