from CSP3_project.models import IV, Wafer, Die
from demonstration_Feb import upload_all
from matplotlib import pyplot as plt


# Uncomment the following line of code if you have NOT already uploaded your documents to the database.
upload_all()

# 1. Plotting all IV experiments from the same wafer onto the same graph

ivs = IV.find(query={'wafer':'wafer_name'})
dataframes = []
for iv in ivs:
    dataframes.append(iv.to_pandas_frame)
for dataframe in dataframes:
    dataframe.plot(x="voltage", y="current")
plt.show()

# 2. Plotting all IV experiments from the same die onto the same graph

ivs = IV.find(query={'die':'die_name'})
dataframes = []
for iv in ivs:
    dataframes.append(iv.to_pandas_frame)
for dataframe in dataframes:
    dataframe.plot(x="voltage", y="current")
plt.show()

# 3. Plotting an IV experiment with an entire knowledge about the die

iv = IV.find_one(query={'die' : 'die_name'})
dataframe = iv.to_pandas_frame
dataframe.plot(x="voltage", y="current")
plt.show()

