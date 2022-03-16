import unittest

from CSP3_project.backend.readers import *

class TestReader(unittest.TestCase):

    def test_get_header(self):
        header_name = "header.csv"
        header_path = Path(__file__).parent.parent.parent / 'CSP3_project' / 'backend' / 'headers' / header_name
        self.assertTrue(str(header_path) == get_header(header_name))

    def test_is_iv_file(self):
        iv_filepath = Path(__file__).parent.parent.parent / 'test_files' / 'IV_wafer_iLGAD_3374-15_die_0_0.txt'
        not_iv_filepath = Path(__file__).parent.parent.parent / 'test_files' / 'labview.log'
        self.assertTrue(is_iv_file(iv_filepath))
        self.assertFalse(is_iv_file(not_iv_filepath))

    def test_iv_reader(self):
        iv_filepath = Path(__file__).parent.parent.parent / 'test_files' / 'IV_wafer_iLGAD_3374-15_die_0_0.txt'
        file_with_missing_value = Path(__file__).parent.parent.parent / 'test_files' / 'Corrupt_IV_wafer_iLGAD_3374-15_die_0_0.txt'
        file_with_missing_required_column = Path(__file__).parent.parent.parent / 'test_files' / 'Corrupt_IV_wafer_iLGAD_3374-15_die_0_1.txt'
        file_with_extra_field = Path(__file__).parent.parent.parent / 'test_files' / 'Corrupt_IV_wafer_iLGAD_3374-15_die_0_3.txt'
        self.assertTrue(iv_reader(iv_filepath))
        self.assertFalse(iv_reader(file_with_missing_value))
        self.assertFalse(iv_reader(file_with_missing_required_column))
        self.assertFalse(iv_reader(file_with_extra_field))


    def test_is_wafer(self):
        #No example wafer files so can't test this
        #wafer_filepath =
        not_wafer_filepath = Path(__file__).parent.parent.parent / 'test_files' / 'IV_wafer_iLGAD_3374-15_die_0_0.txt'
        # self.assertTrue(is_wafer(wafer_filepath))
        self.assertFalse(is_wafer(not_wafer_filepath))

    def test_wafer_reader(self):
        print('No test files')
        #Any example wafer files?
        #wafer_filepath =
        #file_with_missing_component = file with component not in it
        #file_with_no_production_date = file with no production date in it
        #self.assertTrue(wafer_reader(wafer_filepath))
        #self.assertFalse(wafer_reader(file_with_missing_component))
        #self.assertFalse(wafer_reader(file_with_no_production_date))

    def test_is_die(self):
        # No example die files so can't test this
        # die_filepath =
        not_die_filepath = Path(__file__).parent.parent.parent / 'test_files' / 'IV_wafer_iLGAD_3374-15_die_0_0.txt'
        # self.assertTrue(is_die(die_filepath))
        self.assertFalse(is_die(not_die_filepath))

    def die_reader(self):
        print('No test files')
        #Any example die files?
        #die_filepath =
        #file_with_missing_component = file with component not in it
        #self.assertTrue(die_reader(die_filepath))
        #self.assertFalse(die_reader(file_with_missing_component))

if __name__ == '__main__':
    unittest.main()