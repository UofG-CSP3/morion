from .Database import Database, connect
from ..Device import Device
from ..Experiment import Experiment

import unittest


class TestDatabase(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.test_db = connect('test-database')

    @classmethod
    def tearDownClass(cls):
        cls.test_db.experiment_collection.drop()
        cls.test_db.device_collection.drop()
        cls.test_db.disconnect()

    def test_database_connect(self):
        assert self.test_db is not None
        assert self.test_db.dbname == 'test-database'
        print(self.test_db.device_collection)
        print(self.test_db.experiment_collection)

    def test_add_experiment(self):
        self.test_db.add_experiment(Experiment(_id=0,
                                            devices=[],
                                            author="",
                                            timestamp=None,
                                            meta={},
                                            readings=[{}]))
        print(self.test_db.experiment_collection)


    def test_add_device(self):
        self.test_db.add_device(Device(_id='iLGAD577>0_0',
                                        type='wafer',
                                        properties={},
                                        experiments=[]))

        print(self.test_db.device_collection)


if __name__ == '__main__':
    unittest.main(argv=['ignored'], exit=False)