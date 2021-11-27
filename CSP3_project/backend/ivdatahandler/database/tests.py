import unittest

from .Database import connect
from ..Device import Device
from ..Experiment import Experiment


class TestDatabase(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.test_db = connect('test-database')

        cls.test_experiment_data = {'devices': [],
                                    'author': "",
                                    'timestamp': None,
                                    'meta': {},
                                    'readings': [{}]}

    @classmethod
    def tearDownClass(cls):
        cls.test_db.experiment_collection.drop()
        cls.test_db.device_collection.drop()
        cls.test_db.disconnect()

    def test_a_database_connect(self):
        assert self.test_db is not None
        assert self.test_db.dbname == 'test-database'
        # print(self.test_db.device_collection)
        # print(self.test_db.experiment_collection)

    def test_b_add_experiment(self):
        assert self.test_db.add_experiment(Experiment(**self.test_experiment_data)) is not None
        assert self.test_db.find_experiment(self.test_experiment_data) is not None
        print(list(self.test_db.experiment_collection.find()))

    def test_d_add_device(self):
        self.test_db.add_device(Device(_id='iLGAD577>0_0',
                                       type='wafer',
                                       properties={},
                                       experiments=[]))

        # print(list(self.test_db.device_collection.find()))


if __name__ == '__main__':
    unittest.main(argv=['ignored'], exit=False)
