from UofG_PP.models import IV, Die

# 1. Uncomment the following two lines if you need to clean up the database before running this script.
# clear_database()
# upload_all()

# 2. delete_one

# This method will delete one instance of the IV model from the database,
# Since we did not give any parameters, it will delete a random entry.

IV.delete_one()

# Use the parameter to select what entry to delete.
# If more than one entry conforms to the query, delete just one of them.
# If none conform, delete none

IV.delete_one(author='Eren Oezveren')

# 3. delete_many

# This method deletes all entries of IV models that conform to the query from the database

IV.delete_many(author='Eren Oezveren')

# 4. find_one_and_delete

# This method will delete one instance of the Die model that conforms to the query from the database
# and return that instance

Die.find_one_and_delete(size=2.0)

# 5. delete

# This method will delete a model from the database. The method is called on the model that is to be deleted
# after it has been retrieved from the database

iv_of_Danial = IV.find_one(author='Danial Tariq')
iv_of_Danial.delete()
