from datetime import datetime
from typing import Optional

from pydantic import Field, root_validator
from pandas import DataFrame

from morion.mongomodel import MongoModel, BaseModel
from morion.model_decorators import (
    link_one,
    forward_link_one,
    link_many
)


class ExperimentModel(MongoModel):
    """ Specifically for models which have experiment readings, e.g. IV """

    readings: list[BaseModel]  # Override BaseModel with the specific readings you are storing.

    def to_pandas_frame(self) -> DataFrame:
        """Convert readings into a pandas frame"""
        return DataFrame(reading.dict() for reading in self.readings)


class IVModelReadings(BaseModel):
    time: int = Field(alias='t/s')
    voltage: float = Field(alias='U/V')
    currentAverage: float = Field(alias='Iavg/uA')
    currentStdev: float = Field(alias='Istd/uA')
    temperature: float = Field(alias='T/C')
    humidity: float = Field(alias='RH/%')


class IV(ExperimentModel):
    wafer: str
    die: str
    comment: str
    institution: str
    author: str
    date: datetime
    voltageStep: float
    stepDelay: float
    stepMeasurement: int
    compliance: float
    readings: list[IVModelReadings]

    @forward_link_one(lambda: Die)
    def get_die(self):
        return {'wafer': self.wafer, 'name': self.die}


class Die(MongoModel):
    wafer: str
    name: str
    anode_type: str
    device_type: str
    size: float
    pitch: float
    n_channels: float

    @forward_link_one(lambda: Wafer)
    def get_wafer(self):
        return {'name': self.wafer}

    @link_one(IV)
    def get_iv(self):
        return {'wafer': self.wafer, 'die': self.name}


class Wafer(MongoModel):
    name: str
    production_date: datetime
    mask_design: str  # URL to design
    material_type: str
    oxide_thickness: float
    production_run_data: str  # URL to document
    mean_depletion_voltage: float
    depletion_voltage_stdev: float
    thickness: float
    handle_wafer: str
    sheet_resistance: float

    @root_validator
    def set_id(cls, values):
        if values['id'] is None:
            if not values.get('name'):
                return ValueError('Wafer name not provided.')

            values['id'] = values['name']

        return values

    @link_many(Die)
    def get_dies(self):
        return {'wafer': self.name}

    @forward_link_one(lambda: Fabrun)
    def get_fabrun(self):
        return {'wafers': self.name}


class Fabrun(MongoModel):
    name: str
    wafers: list[str]
    type: str
    resistivity: float

    @link_many(Wafer)
    def get_wafers(self):
        return {'name': {"$in": self.wafers}}
