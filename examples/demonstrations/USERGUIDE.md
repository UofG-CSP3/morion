# User Guide Documentation

##### Generation of sample data for IVs, dies, wafers, fabruns
For examples of the generation of Die, Wafer, and IV files, look at the create_test_files.py file in the demonstration folder.
If one already has files set up, create a folder (give it whatever name) and store the files in there. Make sure the newly created folder in next to the morion folder.

##### Uploading data to database
For examples of how uploading works, look at the demonstrate_uploading.py file in the demonstrations folder.
For an example of how a computer may read a file, look at the headers folder in the CSP3_PROJECT folder.
This with readers.py and standard_readers.py will be able to read an iv experiment text file so long as it has a header file to instruct it on how to read an iv experiment file.

##### Downloading data from database
For examples of how uploading works, look at the demonstrate_downloading.py file in the demonstrations folder.
As with above, we have defined our own system of how entries can be downloaded into their own format.
One can see this by observing the writers.py and standard_writers.py files.

##### Linking of IV->Die->Wafer->Fabrun and extracting information on level up / level down
To see how the database schema is structured, look at the models.py file defined in CSP3_PROJECT.
To see an example of how information extracting works with the linking of each layer on a database schema, observe the demonstrate_linking.py folder.
In the case of how we have developed our schema, there are four layers for our database:

1. Fabrun
2. Wafer
3. Die
4. IV

Each layer has access to its own information and information from the layer above or below itself.

##### Plotting IVs
To see examples of how one can plot different IV experiments, look at the demonstrate_graphing.py file.
This file demonstrates three different plotting scenarios:

1. 