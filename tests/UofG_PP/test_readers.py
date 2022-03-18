import unittest

import pydantic
from UofG_PP.readers import *

from . import create_test_files


class TestReader(unittest.TestCase):

    def test_is_iv_file(self):
        iv_filepath = Path(__file__).parent / 'test_files' / 'IV_wafer_iLGAD_3374-15_die_0_0.txt'
        not_iv_filepath = Path(__file__).parent / 'test_files' / 'labview.log'
        create_test_files.create_iv_file("iLGAD_3374-15", "0_0", iv_filepath)
        self.assertTrue(is_iv_file(iv_filepath))
        self.assertFalse(is_iv_file(not_iv_filepath))

    def test_iv_reader(self):
        iv_filepath = Path(__file__).parent / 'test_files' / 'IV_wafer_iLGAD_3374-15_die_0_0.txt'
        corrupt_iv_file = Path(__file__).parent / 'test_files' / 'Corrupt_IV_wafer_iLGAD_3374-15_die_0_0.txt'
        create_test_files.create_iv_file("iLGAD_3374-15", "0_0", iv_filepath)
        create_test_files.create_corrupt_iv_file("iLGAD_3374-15", "0_0", corrupt_iv_file)
        self.assertTrue(iv_reader(iv_filepath))
        self.assertRaises(KeyError, iv_reader, corrupt_iv_file)


    def test_is_wafer(self):
        wafer_filepath = Path(__file__).parent / 'test_files' / 'Wafer1'
        create_test_files.create_wafer_file('iLGAD_3374-15', wafer_filepath)
        not_wafer_filepath = Path(__file__).parent / 'test_files' / 'IV_wafer_iLGAD_3374-15_die_0_0.txt'
        self.assertTrue(is_wafer(wafer_filepath))
        self.assertFalse(is_wafer(not_wafer_filepath))

    def test_wafer_reader(self):
        wafer_filepath = Path(__file__).parent / 'test_files' / 'Wafer1'
        create_test_files.create_wafer_file('iLGAD_3374-15', wafer_filepath)
        corrupt_file = Path(__file__).parent / 'test_files' / 'Wafer2'
        create_test_files.create_corrupt_wafer_file('iLGAD_3374-15', corrupt_file)
        self.assertTrue(wafer_reader(wafer_filepath))
        self.assertRaises(KeyError, wafer_reader, corrupt_file)

    def test_is_die(self):
        die_filepath = Path(__file__).parent / 'test_files' / 'Die1'
        create_test_files.create_die_file('iLGAD_3374-15', 'Die1', die_filepath)
        not_die_filepath = Path(__file__).parent / 'test_files' / 'IV_wafer_iLGAD_3374-15_die_0_0.txt'
        self.assertTrue(is_die(die_filepath))
        self.assertFalse(is_die(not_die_filepath))

    def test_die_reader(self):
        die_filepath = Path(__file__).parent / 'test_files' / 'Die1'
        create_test_files.create_die_file('iLGAD_3374-15', 'Die1', die_filepath)
        file_with_missing_component = Path(__file__).parent / 'test_files' / 'Die2'
        create_test_files.create_corrupt_die_file('iLGAD_3374-15', 'Die2', file_with_missing_component)
        self.assertTrue(die_reader(die_filepath))
        self.assertRaises(pydantic.error_wrappers.ValidationError, die_reader, file_with_missing_component)

if __name__ == '__main__':
    unittest.main()
