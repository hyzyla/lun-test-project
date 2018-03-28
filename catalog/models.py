from sqlalchemy import ForeignKey, Table, case
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.orm import relationship

from . import db


class City(db.Model):
    __tablename__ = 'City'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(256))
    clarification = db.Column(db.String(512))

    groups = relationship('BuildingGroup')

    def __str__(self):
        return "{}{}".format(self.name, ' ({})'.format(self.clarification) if self.clarification else '')


class BuildingGroup(db.Model):
    __tablename__ = 'BuildingGroup'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(1024))
    city_id = db.Column(db.Integer, ForeignKey('City.id'))

    city = relationship('City', back_populates='groups')
    buildings = relationship('Building')

    def __str__(self):
        return self.name


association_table = Table('BuildingFlatXRef', db.metadata,
                          db.Column('building_id', db.Integer, ForeignKey('Building.id')),
                          db.Column('flat_id', db.Integer, ForeignKey('Flat.id'))
                          )


class Building(db.Model):
    __tablename__ = 'Building'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(1024))
    group_id = db.Column(db.Integer, ForeignKey('BuildingGroup.id'))

    group = relationship('BuildingGroup', back_populates='buildings')
    flats = relationship("Flat", secondary=association_table, back_populates='buildings')

    def __str__(self):
        return self.name


class Flat(db.Model):
    __tablename__ = "Flat"

    id = db.Column(db.Integer, primary_key=True)
    room_count = db.Column(db.Integer)
    level_count = db.Column(db.Integer)
    is_studio = db.Column(db.Boolean)
    total_area = db.Column(db.Integer)
    price = db.Column(db.Integer)
    display_per_smeter = db.Column(db.Boolean)
    is_typical = db.Column(db.Boolean)

    buildings = relationship("Building", secondary=association_table, back_populates='flats')

    @hybrid_property
    def full_price(self):
        return self.price if not self.display_per_smeter else self.price * self.total_area

    @full_price.expression
    def full_price(cls):
        return case(
            [
                (Flat.display_per_smeter == True, Flat.total_area * Flat.price, ),
                (Flat.display_per_smeter == False, Flat.price)
            ]
        )