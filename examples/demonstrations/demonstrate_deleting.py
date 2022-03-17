from UofG_PP.models import IV, Die

# 1. First upload a test file (see demonstrate_uploading.py) to test, in this case just upload one file

# 2. delete_one

# This method will delete one instance of the IV model from the database,
# Since we did not give any parameters, it will delete a random entry.

IV.delete_one()

# Use the query='' parameter to select what entry to delete.
# If more than one entry conforms to the query, delete just one of them.
# If none conform, delete none

IV.delete_one(query={'author':'Steve Stevey'})

# 3. delete_many

# This method deletes all entries of IV models that conform to the query from the database

IV.delete_many(query={'author':'Steve Stevey'})

# 4. find_one_and_delete

# This method will delete one instance of the Die model that conforms to the query from the database
# and return that instance

Die.find_one_and_delete(query={'size':2.0})

# 5. delete

# This method will delete a model from the database. The method is called on the model that is to be deleted
# after it has been retrieved from the database

iv_of_Steve = IV.find_one(query={'author':'Steve Stevey'})
iv_of_Steve.delete()
