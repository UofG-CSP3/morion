"""
This module handles set-up of and connection to a MongoDB database.
"""

from configparser import ConfigParser
from dataclasses import dataclass
from typing import Optional

from pymongo import MongoClient
from urllib.parse import urlencode, urlparse, parse_qs, quote_plus

from pymongo.database import Database
from pymongo.uri_parser import parse_uri, InvalidURI


@dataclass
class ConfigInfo:
    """
    This class represents the information needed to connect to the database, taken from the config.ini file
    """
    mongodb_uri: str
    database_name: str


_config_info: Optional[ConfigInfo] = None
_client: Optional[MongoClient] = None
_database: Optional[Database] = None


def setup_config_info(config_info: ConfigInfo):
    global _config_info
    _config_info = config_info


def init_mongo():
    """
    Initialise the MongoDB connection.

    Note: You MUST call setup_config_info before calling this function.
    """

    assert _config_info is not None, "Config Information was not created."
    global _client, _database
    _client = MongoClient(_config_info.mongodb_uri)
    _database = _client[_config_info.database_name]


def database() -> Database:
    assert _database is not None, 'Database connection not established. Have you made sure to call init_mongo()?'
    return _database


def get_config_info() -> ConfigInfo:
    return _config_info


def change_database(new_db_name: str):
    """Change which database in the MongoDB server to use."""
    global _database
    assert _client is not None, 'The MongoDB connection has not yet been initialised.'
    _database = _client[new_db_name]


def format_mongodb_credentials(netloc: str) -> str:
    """
    Properly formats the credentials in the netloc of a MongoDB URI to use percent encoding.

    :param netloc: The netloc field when reading a MongoDB URI using urllib.parse.urlparse
    :return: The netloc modified so that the credentials are correctly formatted.
    """

    def percent_encode_credentials(cred: str):
        return ':'.join([quote_plus(val) for val in cred.split(':')])

    try:
        credentials, rest = netloc.rsplit('@', 1)
    except ValueError:  # No credentials provided.
        return netloc
    else:
        return '@'.join([percent_encode_credentials(credentials), rest])


def mongodb_uri_merge_params(query: str, other_params: dict) -> str:
    """
    Merge the query parameters of a MongoDB URI with a dictionary of other query parameters,

    :param query: The query field when reading a MongoDB URI using urllib.parser.urlparse.
    :param other_params: A dictionary to merge with the MongoDB URI query.
    :return: A formatted query consisting of the two query parameters merged.
    """

    # Based on butla's answer to z4y4ts' question on stack overflow: https://stackoverflow.com/a/52373377
    uri_params = parse_qs(query)
    merged = {**uri_params, **other_params}
    return urlencode(merged, doseq=True)


def mongodb_uri_from_config(config: ConfigParser) -> str:
    """
    Get the MongoDB URI from a ConfigParser.

    Note that if no valid URI could be found, this will instead return `'localhost'`.

    :param config: The ConfigParser to get the MongoDB URI from.
    :return: The MongoDB URI extracted and correctly formatted from the ConfigParser.

    """
    section_name = 'MongoDB Connect'

    uri = config.get(section_name, 'connection', fallback='mongodb://localhost')
    if '://' not in uri:
        uri = 'mongodb://' + uri
    components = urlparse(uri)

    def get_params():
        section = config[section_name] if config.has_section(section_name) else {}
        return {param: value for param, value in section.items() if param != 'connection'}

    formatted_fields = {
        'path': components.path or '/',
        'query': mongodb_uri_merge_params(components.query, get_params())
    }

    if components.scheme.startswith('mongodb'):
        formatted_fields['netloc'] = format_mongodb_credentials(components.netloc)

    return components._replace(**formatted_fields).geturl()


def mongodb_database_name_from_config(config: ConfigParser):
    """
    Get the MongoDB database name to use from a ConfigParser.

    Note that if no name could be found, this will instead return `'database'`.

    :param config: The ConfigParser to get the database name from.
    :return: The database name extracted from config.
    """

    return config.get('MongoDB Database', 'name', fallback='database')

def setup():
    """
    Interactive version of setup_mongodb and setup_mongodb_from_file methods. 
    Asks the user to input options for database connection instantiation one by one.
    Provides the user with an option to save this configuration in a file.
    """

    print("Welcome to Morion configuration wizard. Please follow the instructions below to set up your database connection.")
    uri = input("Please enter your connection string: ")
    while True:
        try:
            if '://' not in uri:
                uri = 'mongodb://' + uri
            parse_uri(uri)
            break
        except InvalidURI:
            uri  = input("Invalid connection string. Please try again: ")
    
    serverselectiontimeoutms = input("Please specify the connection timeout value in milliseconds: ")
    while True:
        try:
            serverselectiontimeoutms = int(serverselectiontimeoutms)
            break
        except:
            serverselectiontimeoutms = input("Invalid value. Please try again: ")

    database_name = input("Please enter the name of the database to connect to: ")

    setup_mongodb(connection=uri, db_name=database_name, connnection_timeout_ms=serverselectiontimeoutms)

    ans = input("The connection has been set up. Would you like to save this configuration in a config.ini file? [y/n] ")

    if ans.strip().lower()[0] == 'y':
        with open('config.ini', 'w') as cfg:
            cfg.write(f"""
[MongoDB Connect]
# Change connection name to your MongoDB connection string.
connection = {uri}

# Example of specifying an additional option.
serverSelectionTimeoutMS = {serverselectiontimeoutms}

# For documentation on how to format connection strings, as well as a list of all additional options,
# see the official MongoDB Documentation: https://docs.mongodb.com/manual/reference/connection-string/

[MongoDB Database]
name = {database_name}
            """)

def setup_mongodb(connection: str = None, db_name: str = 'database', connnection_timeout_ms: int = 5000):
    """
    Will set up and initialise a MongoDB connection given the connection string and database name.

    :param connection: The connection string
    :param db_name: The name of the database
    """

    dummy_config = ConfigParser()
    dummy_config.add_section('MongoDB Connect')
    dummy_config.set('MongoDB Connect', 'connection', connection)
    dummy_config.set('MongoDB Connect', 'serverSelectionTimeoutMS', str(connnection_timeout_ms))

    setup_config_info(ConfigInfo(mongodb_uri=mongodb_uri_from_config(dummy_config), database_name=db_name))
    init_mongo()


def setup_mongodb_from_file(config_file: str):
    """
    Will set up and initialise a MongoDB connection using the given config file.

    :param config_file: The config file containing the necessary information to set up a MongoDB connection.
    """

    config = ConfigParser()
    config.read(config_file)
    uri = mongodb_uri_from_config(config)
    database_name = mongodb_database_name_from_config(config)

    setup_config_info(ConfigInfo(mongodb_uri=uri, database_name=database_name))
    init_mongo()
