import requests
import json
from sqlalchemy.orm import sessionmaker
from database_setup import engine, Planes

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
