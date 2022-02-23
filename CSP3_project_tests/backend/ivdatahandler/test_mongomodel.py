from datetime import datetime
import unittest
import pymongo
import mongomock

from CSP3_project.backend.ivdatahandler import MongoModel
from CSP3_project.backend.models import Wafer, IVModelReadings, Fabrun, Die, IV
from CSP3_project.backend.ivdatahandler.mongomodel import query_merge
from CSP3_project.backend.ivdatahandler.config import get_client, set_client, database,\
    set_database, get_config_info, setup_mongodb, change_database

model = MongoModel()



class TestMongoModel(unittest.TestCase):


    def setUp(self):

        #Connect to db
        try:
            setup_mongodb(connection="mongodb://mongo", db_name='testdb', connnection_timeout_ms=1000)
            get_client().server_info()
        except pymongo.errors.ServerSelectionTimeoutError as err:
            print(err)
            print("Unable to connect to the local database, using a mock database instead...")
            #init mongomock
            set_client(mongomock.MongoClient)
            set_database(mongomock.MongoClient().mockdb)

    def tearDown(self):
        if get_client() is not mongomock.MongoClient:
            get_client().drop_database(get_config_info().database_name)

    def test_collection(self):
        collection = model.collection()
        assert collection is not None

    def test_a_insert(self):
        wafer1 = Wafer(name='aaa', production_date=datetime(year=1999, month=1, day=1),
                       mask_design='https://www.maskdesign.co.uk', material_type='GOLD', oxide_thickness=2.3,
                       production_run_data='https://www.productionrundata.co.uk', mean_depletion_voltage=9.2321,
                       depletion_voltage_stdev=3.21, thickness=3.311,
                       handle_wafer='sagaku', sheet_resistance=31.31)
        die = Die(wafer='a', name='ahb', anode_type='anode', device_type='device', size=2.12, pitch=3.13,
                   n_channels=2.1111334)
        fabrun_with_nonexistent_wafer = Fabrun(name='fabrun1', wafers=['a','b'], type='neutral-good', resistivity=69.42)

        assert(wafer1.insert())
        assert(die.insert())
        die_with_nonexistent_wafer = Die(wafer='aba', name='abc', anode_type='momma', device_type='pappa', size=69.421, pitch=35.23,
                   n_channels=45.133)
        assert(die_with_nonexistent_wafer.insert())

        assert(fabrun_with_nonexistent_wafer.insert())

    def test_a_find_one(self):
        wafer1 = Wafer(name='aaa', production_date=datetime(year=1999, month=1, day=1),
                       mask_design='https://www.maskdesign.co.uk', material_type='GOLD', oxide_thickness=2.3,
                       production_run_data='https://www.productionrundata.co.uk', mean_depletion_voltage=9.2321,
                       depletion_voltage_stdev=3.21, thickness=3.311,
                       handle_wafer='sagaku', sheet_resistance=31.31)
        readings = [IVModelReadings(time=3, voltage=2.0, currentAverage=3.9, currentStdev=4.2, temperature=2.3, humidity=6.9)]
        iv = IV(wafer='aaa', die='abb', comment='HEY', institution='BEY', author='BAE',
                date=datetime(year=2010, month=11, day=10), voltageStep=3.9, stepDelay=4.2, stepMeasurement=4,
                compliance=2.23, readings=readings)
        wafer1.insert()
        iv.insert()

        assert(Wafer.find_one(query={'name':'aaa'})==wafer1)
        assert(IV.find_one(query={'voltageStep':3.9})==iv)

    def test_a_find(self):
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
        assert(len(wafers_GOLD) == 2)
        assert(wafer1 in wafers_GOLD)
        assert(wafer2 in wafers_GOLD)

    def test_delete_one(self):
        die1 = Die(wafer='', name='a', anode_type='anode', device_type='device', size=2.12, pitch=3.13,
                   n_channels=2.1111334)
        die2 = Die(wafer='', name='b', anode_type='anode', device_type='device', size=2.12, pitch=3.13,
                   n_channels=2.1111334)
        die3 = Die(wafer='', name='c', anode_type='anode', device_type='device', size=69.421, pitch=35.23,
                   n_channels=45.133)
        die1.insert()
        die2.insert()
        die3.insert()

        assert(Die.delete_one(query={'size':69.421}))
        assert(Die.find(query={'size':69.421})==())
        assert(len(Die.find(query={}))==2)

    def test_delete_many(self):
        die1 = Die(wafer='aaa', name='abb', anode_type='anode', device_type='device', size=2.12, pitch=3.13,
                   n_channels=2.1111334)
        die2 = Die(wafer='aaa', name='aba', anode_type='anode', device_type='device', size=2.12, pitch=3.13,
                   n_channels=2.1111334)
        die3 = Die(wafer='abc', name='abe', anode_type='anode', device_type='device', size=69.421, pitch=35.23,
                   n_channels=45.133)
        die1.insert()
        die2.insert()
        die3.insert()

        assert(Die.delete_many(query={'wafer': 'aaa'}))
        assert(Die.find(query={'wafer':'aaa'})==())
        assert(len(Die.find(query={}))==1)



    def test_find_one_and_delete(self):
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

        assert(Wafer.find_one_and_delete(query={'name':'a'})==wafer1)
        assert(Wafer.find_one(query={'name':'aaa'}) is None)


    def test_update(self):
        die = Die(wafer='bbb', name='die', anode_type='anodDD', device_type='deDDvice', size=69.21, pitch=35.23,
                   n_channels=45.133)
        die.insert()
        id = die.id
        die_update = Die(id=id, wafer='bbb', name='updated_die', anode_type='anodDD', device_type='deDDvice', size=69.23, pitch=35.23,
                   n_channels=45.133)

        assert(die_update.update())
        all_dies = Die.find()
        assert(die_update in all_dies)
        assert(die not in all_dies)

    def test_insert_or_replace(self):
        die = Die(wafer='bbb', name='a', anode_type='anode', device_type='device', size=2.12, pitch=3.13,
                   n_channels=3.25)
        assert (die.insert_or_replace())
        replacement_die = Die(id=die.id, wafer='bbb', name='a', anode_type='anode', device_type='device', size=2.12,
                      pitch=3.13,
                      n_channels=3.15)
        assert (replacement_die.insert_or_replace())
        assert (replacement_die in Die.find())
        assert (die not in Die.find())
    #def test_find_and_replace(self):
     #   die1 = Die(wafer='aaa', name='a', anode_type='anode', device_type='device', size=2.12, pitch=3.13,
      #            n_channels=2.1111334)
       # die2 = Die(wafer='bbb', name='b', anode_type='anode', device_type='device', size=2.12, pitch=3.13,
        #           n_channels=3.25)
        #print (die2.find_and_replace(, query={'name': 'a'}))
        #assert (die1 not in Die.find())

    def test_delete(self):
        wafer = Wafer(name='aaa', production_date=datetime(year=1999, month=1, day=1),
                       mask_design='https://www.maskdesign.co.uk', material_type='GOLD', oxide_thickness=2.3,
                       production_run_data='https://www.productionrundata.co.uk', mean_depletion_voltage=9.2321,
                       depletion_voltage_stdev=3.21, thickness=3.311,
                       handle_wafer='sagaku', sheet_resistance=31.31)
        wafer.insert()

        wafer.delete()
        assert(Wafer.find(query={})==())

    def test_query_merge(self):
        query1 = {'name': 'a'}
        assert(query_merge(query = query1, wafer = 'b', voltage = 3.1) == {'name': 'a', 'wafer': 'b', 'voltage': 3.1})

