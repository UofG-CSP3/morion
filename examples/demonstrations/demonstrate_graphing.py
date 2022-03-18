from CSP3_project.models import IV, Wafer, Die
from demonstration_Feb import upload_all
from matplotlib import pyplot as plt


# Uncomment the following line of code if you have NOT already uploaded your documents to the database.
#upload_all()

# 1. Plotting all IV experiments from the same wafer onto the same graph

#Wafer you want to get IVs from:
wafer_name = 'INSERT WAFER NAME HERE'
wafer = Wafer.find_one(wafer=wafer_name)
#IVs on wafer:
ivs = IV.find(wafer='wafer_name')
#Plotting the IV experiments
dataframes = []
for iv in ivs:
    dataframes.append(iv.to_pandas_frame())
for dataframe in dataframes:
    dataframe.plot(x="voltage", y="current")
plt.show()

# 2. Plotting all IV experiments from the same die onto the same graph

#Die you want to get IVs from:
die_name = 'INSERT DIE NAME HERE'
die = Die.find_one(die=die_name)
#IVs on die:
ivs = IV.find(die='die_name')
#Plotting the IV experiments
dataframes = []
for iv in ivs:
    dataframes.append(iv.to_pandas_frame())
for dataframe in dataframes:
    dataframe.plot(x="voltage", y="current")
plt.show()

# 3. Plotting an IV experiment with an entire knowledge about the die

#Die you want to get IV from:
die_name = 'INSERT DIE NAME HERE'
die = Die.find_one(die=die_name)
#IV on die:
iv = IV.find_one(die='die_name')
#Plotting the IV experiment:
dataframe = iv.to_pandas_frame()
dataframe.plot(x="voltage", y="current")
plt.show()
#Print die information:
print(die)
#Print experiment information:
print(dataframe)
#Print wafer that die is on:
wafer = die.get_wafer()
print(wafer)
#Print fabrun that wafer is on:
fabrun = wafer.get_fabrun()
print(fabrun)



