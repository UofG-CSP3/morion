import unittest
import pymongo
from pathlib import Path
from configparser import ConfigParser
from morion.config import *

class TestConfig(unittest.TestCase):

    def setUp(self):
        self.example_config1 = ConfigParser()
        self.example_config2 = ConfigParser()
        self.example_config3 = ConfigParser()

        for config in (self.example_config1, self.example_config2, self.example_config3):
            config.add_section("MongoDB Connect")
            config.add_section("MongoDB Database")
            
        self.example_config1.set("MongoDB Connect", "connection", "localhost")
        self.example_config2.set("MongoDB Connect", "connection", "mongodb://mongo")
        self.example_config3.set("MongoDB Connect", "connection", "mongodb://lögín:páßwörd@example.domain.name.com")

        self.example_config1.set("MongoDB Connect", "serverSelectionTimeoutMS", "1000")
        self.example_config2.set("MongoDB Connect", "serverSelectionTimeoutMS", "5000")
        self.example_config3.set("MongoDB Connect", "serverSelectionTimeoutMS", "200")

        self.example_config1.set("MongoDB Database", "name", "test")
        # self.example_config2.set("MongoDB Database", "name", "")
        self.example_config3.set("MongoDB Database", "name", "test_database")


    def tearDown(self):
        pass

    def test_setup_mongodb(self):
        setup_mongodb(connection="login:password@192.168.0.1", db_name="test_setup_mongodb", connnection_timeout_ms=2137)
        self.assertTrue(get_config_info().mongodb_uri == "mongodb://login:password@192.168.0.1/?serverselectiontimeoutms=2137")
        self.assertTrue(get_config_info().database_name == "test_setup_mongodb")

    def test_setup_mongodb_from_file(self):
        setup_mongodb_from_file(str((Path(__file__).parents[2] / 'src' / 'morion' / 'config.ini').resolve()))
        self.assertTrue(get_config_info().mongodb_uri == "mongodb://mongo/?serverselectiontimeoutms=1000")
        self.assertTrue(get_config_info().database_name == "database")

    def test_mongodb_database_name_from_config(self):
        database_name1 = mongodb_database_name_from_config(self.example_config1)
        database_name2 = mongodb_database_name_from_config(self.example_config2)
        database_name3 = mongodb_database_name_from_config(self.example_config3)
        self.assertTrue(database_name1 == "test")
        self.assertTrue(database_name2 == "database")
        self.assertTrue(database_name3 == "test_database")

    def test_mongodb_uri_merge_params(self):
        query = "a=32&d=48&f=10"
        other_params = {'b' : '30', 'c' : '56', 'e': '49'}
        merged = mongodb_uri_merge_params(query=query, other_params=other_params)
        self.assertTrue(merged == "a=32&d=48&f=10&b=30&c=56&e=49")

    def test_format_mongodb_credentials(self):
        netloc = "żółć:jaźń@very.cool.url.com"
        formatted = format_mongodb_credentials(netloc=netloc)
        self.assertTrue(formatted == "%C5%BC%C3%B3%C5%82%C4%87:ja%C5%BA%C5%84@very.cool.url.com")

    def test_change_database(self):
        change_database("i_love_writing_unit_tests")
        self.assertTrue(database().name == "i_love_writing_unit_tests")

    def test_mongodb_uri_from_config(self):
        uri1 = mongodb_uri_from_config(self.example_config1)
        uri2 = mongodb_uri_from_config(self.example_config2)
        uri3 = mongodb_uri_from_config(self.example_config3)
        self.assertTrue(uri1 == "mongodb://localhost/?serverselectiontimeoutms=1000")
        self.assertTrue(uri2 == "mongodb://mongo/?serverselectiontimeoutms=5000")
        self.assertTrue(uri3 == "mongodb://l%C3%B6g%C3%ADn:p%C3%A1%C3%9Fw%C3%B6rd@example.domain.name.com/?serverselectiontimeoutms=200")

if __name__=='__main__':
    unittest.main()