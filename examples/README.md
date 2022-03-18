## Running the examples

Install the `UofG_PP` and `morion` packages by running `pip install .` in the base directory first.

## Setting up the database

Open the python shell and run 
```python
>>> from morion import setup
>>> setup()
```
It will ask you to set the variables `connection` and `database`. Assign `connection` to the MongoDB
uri you want to connect to. For example, your uri may look something like `mongodb://<username>:<password>@<url>`.


Similarly, set the `database` variable to which database in your MongoDB server you want to use.

