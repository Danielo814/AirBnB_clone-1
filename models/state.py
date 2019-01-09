#!/usr/bin/python3
"""This is the state class"""
from models.base_model import BaseModel, Base
from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
import os

class State(BaseModel, Base):
    """This is the class for State
    Attributes:
        name: input name
    """
    if os.getenv("HBNB_TYPE_STORAGE") == "db":
        __tablename__ = "states"
        name = Column(String(128), nullable=False)
        cities = relationship("City", cascade="all, delete-orphan", backref="state")

    else:

        """File Storage"""
        @property
        def cities(self):
            """
            city properties
            """
            cls = []
            for val in storage.all(City).values():
                if val.state_id == self.id:
                    cls.append(val)
            return cls
