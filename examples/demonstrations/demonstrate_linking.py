from UofG_PP.models import IV, Wafer, Die
from demonstration_Feb import upload_all


# Uncomment the following line of code if you have NOT already uploaded your documents to the database.
# upload_all()

# 1. Basic Linking

# Suppose that we have a die, and we want to get the wafer which it is on.

# Get a die
die = Die.find_one() # <- This will give us an arbitrary Die from the database

# To get the wafer which this die is on, simply use the .get_wafer() function.

wafer = die.get_wafer()

# You can print the wafer to verify that you got it from the database.
# If the wafer could not be found, None will be returned instead.
print(wafer)

# We can also do the inverse, given a wafer we can get all the dies that were on that wafer.
# This will return an array of all the dies on this wafer.
dies = wafer.get_dies()

# Let us verify that the original die we had is in this list
# The below should print 'True' is our original die was in the list
print(die in dies)


# 2. Chaining

# You can also of course chain links together

# Let us get an arbitrary IV
iv = IV.find_one()

# To obtain the wafer for this iv, we first obtain the die it was performed on, and then the wafer which the die is on
iv_wafer = iv.get_die().get_wafer()
