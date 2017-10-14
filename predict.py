# Imports
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Float, Boolean, BigInteger

# Configuring DB Conx
engine = create_engine("postgresql://@localhost/planes")
Base = declarative_base()


# Setting up DB Schema
class Planes(Base):
    __tablename__ = 'predictions'
    
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



import requests
import json
from sqlalchemy.orm import sessionmaker

Session = sessionmaker(bind=engine)
session = Session()

url = "https://public-api.adsbexchange.com/VirtualRadar/AircraftList.json?trFmt=sa"

#getting around dictionaries with missing keys
def safe_key(key, dict):
    if key in dict:
        return dict[key]
    else:
        return None

#getting around annoying mistakes in the dataset
def extra_safe_key(key, dict):
    if safe_key(key, dict) == None:
        return None
    elif type(safe_key(key, dict)) != int:
        return None
    else:
        return safe_key(key, dict)

#Updating DB function
def update():
    info = requests.get(url)

    #adding the data to the database
    if (info.ok):
        data = info.json()['acList']
        for n in range(len(data)):
            plane = data[n]
            alt = safe_key('Alt', plane)
            galt = safe_key('GAlt', plane)
            inhg = safe_key('InHG', plane)
            altt = safe_key('AltT', plane)
            lat = safe_key('Lat', plane)
            long = safe_key('Long', plane)
            postime = safe_key('PosTime', plane)
            mlat = safe_key('Mlat', plane)
            spd = safe_key('Spd', plane)
            spdtyp = safe_key('SpdTyp', plane)
            trak = safe_key('Trak', plane)
            trkh = safe_key('TrkH', plane)
            type = safe_key('Type', plane)
            mdl = safe_key('Mdl', plane)
            man = safe_key('Man', plane)
            year = extra_safe_key('Year', plane)
            vsi = safe_key('Vsi', plane)
            vsit = safe_key('VsiT', plane)
            species = safe_key('Species', plane)
            engtype = safe_key('EngType', plane)
            engmount = safe_key('EngMount', plane)
            engines = safe_key('Engines', plane)
            mil = safe_key('Mil', plane)
            cou = safe_key('Cou', plane)
            gnd = safe_key('Gnd', plane)
            flightscount = safe_key('FlightsCount', plane)
            interested = safe_key('Interested', plane)
            talt = safe_key('Talt', plane)
            ttrk = safe_key('Ttrk', plane)
            wtc = safe_key('WTC', plane)
            row = Planes(alt=alt, galt=galt, inhg=inhg, altt=altt, lat=lat, \
                         long=long, postime=postime, mlat=mlat, spd=spd, spdtyp=spdtyp, \
                         trak=trak, trkh = trkh, type=type, mdl=mdl, man=man, year=year, \
                         vsi=vsi, vsit=vsit, species=species, engtype=engtype, engmount=engmount, \
                         engines=engines, mil=mil, cou=cou, gnd=gnd, flightscount=flightscount, \
                         interested=interested, talt=talt, wtc=wtc)
            session.add(row)
            session.commit()
    else:
        info.raise_for_status()

#pull and store updated data
update()            


import psycopg2
import pandas
import numpy
from numpy import nan
from sklearn.preprocessing import Imputer
from pandas.tools.plotting import scatter_matrix
import matplotlib.pyplot as plt
from sklearn import model_selection
from sklearn.metrics import classification_report
from sklearn.metrics import confusion_matrix
from sklearn.metrics import accuracy_score
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis
from sklearn.naive_bayes import GaussianNB
from sklearn.svm import SVC
from sklearn.tree import DecisionTreeRegressor

#connecting to database
conn = psycopg2.connect(dbname="planes")

#converting table into dataframe
df = pandas.DataFrame()
for chunk in pandas.read_sql('select * from plane_table', con=conn, chunksize=5000):
    df = df.append(chunk)

#replacing Null values by NaN
df.fillna(value=nan, inplace=True)

#split dataset into X and Y
array = df.values

#only considering columns with numerical values for now
X = numpy.column_stack((array[:,0:8],array[:,9:12],array[:,16:22],array[:,26],array[:,28:30]))

#replacing NaN values by mean values
imputer = Imputer()
transformed_X = imputer.fit_transform(X)

Y = array[:,30]
Y = Y.astype('int')

# train on original dataset
cr = DecisionTreeClassifier()
cr.fit(transformed_X, Y)




#connecting to database
conn = psycopg2.connect(dbname="planes")

#converting table into dataframe
df = pandas.DataFrame()
for chunk in pandas.read_sql('select * from predictions', con=conn, chunksize=5000):
    df = df.append(chunk)

#replacing Null values by NaN
df.fillna(value=nan, inplace=True)

#split dataset to train models
array = df.values

#only considering columns with numerical values for now
X = numpy.column_stack((array[:,0:8],array[:,9:12],array[:,16:22],array[:,26],array[:,28:30]))

#replacing NaN values by mean values
imputer = Imputer()
transformed_X = imputer.fit_transform(X)

Y = array[:,30]
Y = Y.astype('int')

predictions = cr.predict(transformed_X)
print(accuracy_score(Y, predictions))
print(confusion_matrix(Y, predictions))
print(classification_report(Y, predictions))
