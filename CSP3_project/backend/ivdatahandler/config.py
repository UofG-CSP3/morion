from configparser import ConfigParser
from dataclasses import dataclass
from typing import Optional

from pymongo import MongoClient
from urllib.parse import urlencode, urlparse, parse_qs, quote_plus

from pymongo.database import Database


@dataclass
class ConfigInfo:
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
    assert (_database is not None,
            'Database connection has not been established. Have you made sure to call init_mongo()?')
    return _database


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

    uri = config.get(section_name, 'connection', fallback='localhost')
    components = urlparse(uri)

    def get_params():
        section = config[section_name] if config.has_section(section_name) else {}
        return {param: value for param, value in section.items() if param != 'connection'}

    print(components.path)

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
