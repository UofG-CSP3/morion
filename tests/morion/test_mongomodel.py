from datetime import datetime
import unittest
import pymongo
import mongomock

from morion import MongoModel
from CSP3_project.models import Wafer, IVModelReadings, Fabrun, Die, IV
from morion.mongomodel import query_merge
from morion.config import get_config_info, setup_mongodb, change_database
import morion.config as config

model = MongoModel()


class TestMongoModel(unittest.TestCase):

    def setUp(self):

        # Connect to db
        try:
            setup_mongodb(connection="mongodb://mongo", db_name='testdb', connnection_timeout_ms=1000)
            config._client.server_info()
        except pymongo.errors.ServerSelectionTimeoutError as err:
            print(err)
            print("Unable to connect to the local database, using a mock database instead...")
            # init mongomock
            config._client = mongomock.MongoClient
            config._database = mongomock.MongoClient().mockdb

    def tearDown(self):
        if config._client is not mongomock.MongoClient:
            config._client.drop_database(get_config_info().database_name)

    def test_collection(self):
        """
        Tests that the collection function does not return None
        """
        collection = model.collection()
        self.assertTrue(collection is not None)

    def test_a_insert(self):
        """
        Tests insert() by inserting to the db
            1. a wafer
            2. a die that with an existent wafer
            3. a die with a nonexistent wafer
            4. a fabrun with nonexistent wafer

        and asserting that the insertion was acknowledged by the database.
        """
        wafer1 = Wafer(name='aaa', production_date=datetime(year=1999, month=1, day=1),
                       mask_design='https://www.maskdesign.co.uk', material_type='GOLD', oxide_thickness=2.3,
                       production_run_data='https://www.productionrundata.co.uk', mean_depletion_voltage=9.2321,
                       depletion_voltage_stdev=3.21, thickness=3.311,
                       handle_wafer='sagaku', sheet_resistance=31.31)
        die = Die(wafer='a', name='ahb', anode_type='anode', device_type='device', size=2.12, pitch=3.13,
                  n_channels=2.1111334)
        fabrun_with_nonexistent_wafer = Fabrun(name='fabrun1', wafers=['a', 'b'], type='neutral-good',
                                               resistivity=69.42)

        self.assertTrue(wafer1.insert())
        self.assertTrue(die.insert())
        die_with_nonexistent_wafer = Die(wafer='aba', name='abc', anode_type='momma', device_type='pappa', size=69.421,
                                         pitch=35.23,
                                         n_channels=45.133)
        self.assertTrue(die_with_nonexistent_wafer.insert())

        self.assertTrue(fabrun_with_nonexistent_wafer.insert())

    def test_a_find_one(self):
        """
        Tests find_one() by inserting a wafer and an iv into the db and asserting that
        the wafer and iv found by find_one() are the ones that were inserted.

        """
        wafer = Wafer(name='aaa', production_date=datetime(year=1999, month=1, day=1),
                       mask_design='https://www.maskdesign.co.uk', material_type='GOLD', oxide_thickness=2.3,
                       production_run_data='https://www.productionrundata.co.uk', mean_depletion_voltage=9.2321,
                       depletion_voltage_stdev=3.21, thickness=3.311,
                       handle_wafer='sagaku', sheet_resistance=31.31)

        readings = [
            IVModelReadings(time=3, voltage=2.0, currentAverage=3.9, currentStdev=4.2, temperature=2.3, humidity=6.9)]

        iv = IV(wafer='aaa', die='abb', comment='HEY', institution='BEY', author='BAE',
                date=datetime(year=2010, month=11, day=10), voltageStep=3.9, stepDelay=4.2, stepMeasurement=4,
                compliance=2.23, readings=readings)

        wafer.insert()
        iv.insert()

        self.assertEqual(Wafer.find_one(query={'name': 'aaa'}),wafer)
        self.assertEqual(IV.find_one(query={'voltageStep': 3.9}),iv)

    def test_a_find(self):
        """
        Tests find() by inserting into the db two wafers with the same material_type,
        using find() to find all wafers with that material_type and then asserting
        that find() returns those two inserted wafers.
        """
        wafer1 = Wafer(name='aaa', production_date=datetime(year=1999, month=1, day=1),
                       mask_design='https://www.maskdesign.co.uk', material_type='GOLD', oxide_thickness=2.3,
                       production_run_data='https://www.productionrundata.co.uk', mean_depletion_voltage=9.2321,
                       depletion_voltage_stdev=3.21, thickness=3.311,
                       handle_wafer='sagaku', sheet_resistance=31.31)
        wafer2 = Wafer(name='bbb', production_date=datetime(year=1999, month=1, day=1),
                       mask_design='https://www.maskdesign.co.uk', material_type='GOLD', oxide_thickness=2.3,
                       production_run_data='https://www.productionrundata.co.uk', mean_depletion_voltage=9.2321,
                       depletion_voltage_stdev=3.21, thickness=3.311,
                       handle_wafer='sagaku', sheet_resistance=31.31)
        wafer1.insert()
        wafer2.insert()

        wafers_GOLD = Wafer.find(query={'material_type': 'GOLD'})
        self.assertEqual(len(wafers_GOLD),2)
        self.assertTrue(wafer1 in wafers_GOLD)
        self.assertTrue(wafer2 in wafers_GOLD)

    def test_delete_one(self):
        """
        Tests delete_one() by inserting three different dies into the db,
        deleting a specific one using delete_one() and asserting that
        the deletion was acknowledged, we cannot find that die in the db anymore and
        there are two dies left in the db.
        """
        die1 = Die(wafer='', name='a', anode_type='anode', device_type='device', size=2.12, pitch=3.13,
                   n_channels=2.1111334)
        die2 = Die(wafer='', name='b', anode_type='anode', device_type='device', size=2.12, pitch=3.13,
                   n_channels=2.1111334)
        die3 = Die(wafer='', name='c', anode_type='anode', device_type='device', size=69.421, pitch=35.23,
                   n_channels=45.133)
        die1.insert()
        die2.insert()
        die3.insert()

        self.assertTrue(Die.delete_one(query={'size': 69.421}))
        self.assertEqual(Die.find(query={'size': 69.421}),())
        self.assertEqual(len(Die.find(query={})),2)

    def test_delete_many(self):
        """
        Tests delete_many() by inserting three different dies into the db, two of those having the same wafer.
        Then deleting all those dies with that wafer, it asserts the deletion was acknowledged,
        there are no more dies with that wafer in the db and there is exactly one die left in the db.
        """
        die1 = Die(wafer='aaa', name='abb', anode_type='anode', device_type='device', size=2.12, pitch=3.13,
                   n_channels=2.1111334)
        die2 = Die(wafer='aaa', name='aba', anode_type='anode', device_type='device', size=2.12, pitch=3.13,
                   n_channels=2.1111334)
        die3 = Die(wafer='abc', name='abe', anode_type='anode', device_type='device', size=69.421, pitch=35.23,
                   n_channels=45.133)
        die1.insert()
        die2.insert()
        die3.insert()

        self.assertTrue(Die.delete_many(query={'wafer': 'aaa'}))
        self.assertEqual(Die.find(query={'wafer': 'aaa'}),())
        self.assertEqual(len(Die.find(query={})),1)

    def test_find_one_and_delete(self):
        """
        Tests find_one_and_delete() by inserting two wafers into the db, using find_one_and_delete() with a query specific
        to one of the wafers, then asserting that find_one_and_delete() returns that specific wafer,
        and that wafer cannot be found in the db anymore.

        """
        wafer1 = Wafer(name='a', production_date=datetime(year=1999, month=1, day=1),
                       mask_design='https://www.maskdesign.co.uk', material_type='GOLD', oxide_thickness=2.3,
                       production_run_data='https://www.productionrundata.co.uk', mean_depletion_voltage=9.2321,
                       depletion_voltage_stdev=3.21, thickness=3.311,
                       handle_wafer='sagaku', sheet_resistance=31.31)

        wafer2 = Wafer(name='b', production_date=datetime(year=1999, month=1, day=1),
                       mask_design='https://www.maskdesign.co.uk', material_type='GOLD', oxide_thickness=2.3,
                       production_run_data='https://www.productionrundata.co.uk', mean_depletion_voltage=9.2321,
                       depletion_voltage_stdev=3.21, thickness=3.311,
                       handle_wafer='sagaku', sheet_resistance=31.31)

        wafer1.insert()
        wafer2.insert()

        self.assertEqual(Wafer.find_one_and_delete(query={'name': 'a'}),wafer1)
        self.assertTrue(Wafer.find_one(query={'name': 'aaa'}) is None)

    def test_update(self):
        """
        Tests update() by inserting a die
        """
        die = Die(wafer='bbb', name='die', anode_type='anodDD', device_type='deDDvice', size=69.21, pitch=35.23,
                  n_channels=45.133)
        die.insert()
        id = die.id
        die_update = Die(id=id, wafer='bbb', name='updated_die', anode_type='anodDD', device_type='deDDvice',
                         size=69.23, pitch=35.23,
                         n_channels=45.133)

        self.assertTrue(die_update.update())
        all_dies = Die.find()
        self.assertTrue(die_update in all_dies)
        self.assertTrue(die not in all_dies)

    def test_insert_or_replace(self):
        """
        Tests insert_or_replace() by first using it to insert a die, asserting the operation is acknowledged.
        Then it creates a replacement die changing the anode_type but keeping the same id as the first die,
        then uses insert_or_replace() to put the new die in the db and remove the old one,
        asserting that the operation is acknowledged, the replacement die can be found in the db,
        and the first die cannot be found in the db.
        """
        die = Die(wafer='bbb', name='a', anode_type='anode', device_type='device', size=2.12, pitch=3.13,
                  n_channels=3.25)
        self.assertTrue(die.insert_or_replace())
        replacement_die = Die(id=die.id, wafer='bbb', name='a', anode_type='anode', device_type='device', size=2.12,
                              pitch=3.13,
                              n_channels=3.15)
        self.assertTrue(replacement_die.insert_or_replace())
        self.assertTrue(replacement_die in Die.find())
        self.assertTrue(die not in Die.find())

    def test_find_and_replace(self):
        """
        Tests find_and_replace() by having an old die in the db, then using find_and_replace
        to find and replace that die with a new one, that had not been yet inserted into the db,
        asserting that the method returns the old die, that it cannot be found in the db anymore,
        that the only die in the db is the new die and that its id has been changed to that of
        the old die.
        Further tests replacing a die in the db with a die taken directly from the db with Die.find_one.

        """
        old_die = Die(wafer='aaa', name='a', anode_type='anode', device_type='device', size=2.12, pitch=3.13,
               n_channels=2.1111334)
        new_die = Die(wafer='bbb', name='b', anode_type='anode', device_type='device', size=2.12, pitch=3.13,
              n_channels=3.25)
        old_die.insert()
        self.assertEqual(new_die.find_and_replace(query={'name': 'a'}),old_die)
        self.assertTrue(old_die not in Die.find())
        self.assertEqual(len(Die.find()),1)
        new_die.id = old_die.id
        self.assertEqual(Die.find_one(query={}),new_die)
        self.assertTrue(Die.find_one().id==old_die.id)
        die3 = Die(wafer='aaa', name='c', anode_type='anode', device_type='device', size=2.12, pitch=3.13,
                   n_channels=2.1111334)
        die3.insert()
        die_from_db = Die.find_one(query={'name' : 'b'})
        self.assertEqual(die_from_db.find_and_replace(query={'name': 'c'}),die3)
        self.assertTrue(die3 not in Die.find())


    def test_delete(self):
        """
        Tests delete() by inserting a wafer, deleting it and then asserting that no wafer can be found in the db.
        """
        wafer = Wafer(name='aaa', production_date=datetime(year=1999, month=1, day=1),
                      mask_design='https://www.maskdesign.co.uk', material_type='GOLD', oxide_thickness=2.3,
                      production_run_data='https://www.productionrundata.co.uk', mean_depletion_voltage=9.2321,
                      depletion_voltage_stdev=3.21, thickness=3.311,
                      handle_wafer='sagaku', sheet_resistance=31.31)
        wafer.insert()

        wafer.delete()
        self.assertEqual(Wafer.find(query={}),())

    def test_query_merge(self):
        """
        Tests query_merge() by asserting that a query and
        two additional queries are being merged into a single dictionary.
        """
        query1 = {'name': 'a'}
        self.assertEqual(query_merge(query=query1, wafer='b', voltage=3.1),{'name': 'a', 'wafer': 'b', 'voltage': 3.1})

    def test_no_validate_construct(self):
        """
        Tests no_validate_construct() by putting a Die object in the database, retrieving it in the form of a dictionary, constructing
        a new object from it using no_validate_construct() and comparing it to the old one.
        """
        die = Die(wafer='lorem', name='ipsum', anode_type='dolor', device_type='sit', size=24.45, pitch=51.51, n_channels=3.1415)
        die.insert()

        die_dict = Die.collection().find_one({'wafer': 'lorem'})
        restored_die = Die.no_validate_construct(die_dict)
        self.assertTrue(die == restored_die)

if __name__=='__main__':
    unittest.main()