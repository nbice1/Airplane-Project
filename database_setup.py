# Imports
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Float, Boolean, BigInteger

# Configuring DB Conx
engine = create_engine("postgresql://@localhost/planes")
Base = declarative_base()


# Setting up DB Schema
class Planes(Base):
    __tablename__ = 'plane_table'
    
    id = Column(Integer, primary_key=True)
    alt = Column(Integer)
    galt = Column(Integer)
    inhg = Column(Float)
    altt = Column(Integer)
    lat = Column(Float)
    long = Column(Float)
    postime = Column(BigInteger)
    mlat = Column(Boolean)
    spd = Column(Float)
    spdtyp = Column(Integer)
    trak = Column(Float)
    trkh = Column(Boolean)
    type = Column(String)
    mdl = Column(String)
    man = Column(String)
    year = Column(Integer)
    vsi = Column(Integer)
    vsit = Column(Integer)
    species = Column(Integer)
    engtype = Column(Integer)
    engmount = Column(Integer)
    engines = Column(String)
    mil = Column(Boolean)
    cou = Column(String)
    gnd = Column(Boolean)
    flightscount = Column(Integer)
    interested = Column(Boolean)
    talt = Column(Float)
    ttrk = Column(Float)
    wtc = Column(Integer)
    

# Instantiating the DB
Base.metadata.create_all(engine)
