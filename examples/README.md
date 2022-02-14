## Running the examples

The scripts in this example folder need to be able to import packages from within the
`CSP3_project/` directory:
Here are two ways in which you can go about doing this: 
1. Simply copy/paste the scripts into the `CSP3_project/` directory and run them from there. 
This is probably the easiest way.
2. Add the `CSP3_project/` directory to `sys.path`. 
Here's a [stack overflow](https://stackoverflow.com/a/4383597) which you can use to guide you.

## Setting up the database

Navigate to `CSP3_project/backend/ivdatahandler/` and open the `config.ini` file.
In it, you should see the variables `connection` and `database`. Assign `connection` to the MongoDB
uri you want to connect to. For example, your uri may look something like `mongodb://<username>:<password>@<url>`,
in which case you `config.ini` should have the line `connection = mongodb://<username>:<password>@<url>`.


Similarly, set the `database` variable to which database in your MongoDB server you want to use.

