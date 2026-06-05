import sqlite3
from geopy.geocoders import Nominatim

## Initial Base Users
conn = sqlite3.connect('R4SM_lib/data/Users.sqlite')
curr = conn.cursor()
curr.execute("CREATE TABLE IF NOT EXISTS users(login text, password text, familyname text, firstname text)")
curr.execute("""
    INSERT INTO users VALUES
        ('TestAdmin@test.com', 'Pass1234!', 'Test', 'Admin')
""")
conn.commit()
conn.close()

## Initial Base R4SDB
conn = sqlite3.connect('R4SM_lib/data/R4SDB.sqlite')
conn.enable_load_extension(True)
conn.load_extension(r"R4SM_lib/modules/mod_spatialite.dll")
curr = conn.cursor()
curr.execute("SELECT InitSpatialMetaData(1)")
# Headquarters
curr.execute("""
             CREATE TABLE IF NOT EXISTS headquarters(
             id INTEGER PRIMARY KEY,
             name text,
             city text,
             road text,
             building_nr text)
             """)
curr.execute("""
    SELECT AddGeometryColumn(
        'headquarters',
        'geo',
        4326,
        'POINT',
        'XY'
    )
""")
API = Nominatim(user_agent='App')
name = 'Rent 4 Sport'
city = 'Warszawa'
road = 'Aleje Jerozolimskie'
building_nr = '5'
address = f'{city}, {road} {building_nr}'
location = API.geocode(address)
point_wkt = f"POINT({location.longitude} {location.latitude})"
curr.execute("""
INSERT INTO headquarters(name, city, road, building_nr, geo)
VALUES (
    ?,
    ?,
    ?,
    ?,
    ST_GeomFromText(?, 4326)
)
""",(name,city,road,building_nr,point_wkt))
# Rental
curr.execute("""
             CREATE TABLE IF NOT EXISTS rental(
             id INTEGER PRIMARY KEY,
             name text,
             city text,
             road text,
             building_nr text,
             headqoters_id INTEGER)
             """)
curr.execute("""
    SELECT AddGeometryColumn(
        'rental',
        'geo',
        4326,
        'POINT',
        'XY'
    )
""")
API = Nominatim(user_agent='App')
name = 'Rent 4 Sport'
city = 'Warszawa'
road = 'Adama Mickiewicza'
building_nr = '10'
headqoters_id = 1
address = f'{city}, {road} {building_nr}'
location = API.geocode(address)
point_wkt = f"POINT({location.longitude} {location.latitude})"
curr.execute("""
INSERT INTO rental(name, city, road, building_nr,headqoters_id, geo)
VALUES (
    ?,
    ?,
    ?,
    ?,
    ?,
    ST_GeomFromText(?, 4326)
)
""",(name,city,road,building_nr,headqoters_id,point_wkt))
# Employee
curr.execute("""
             CREATE TABLE IF NOT EXISTS employee(
             id INTEGER PRIMARY KEY,
             firstname text,
             familyname text,
             name text,
             city text,
             road text,
             building_nr text,
             headqoters_id INTEGER,
             rental_id INTEGER)
             """)
curr.execute("""
    SELECT AddGeometryColumn(
        'employee',
        'geo',
        4326,
        'POINT',
        'XY'
    )
""")
API = Nominatim(user_agent='App')
firstname = 'Jan'
familyname = 'Kowalski'
city = 'Warszawa'
road = 'Deotymy'
building_nr = '3'
headqoters_id = 1
rental_id = 1
address = f'{city}, {road} {building_nr}'
location = API.geocode(address)
point_wkt = f"POINT({location.longitude} {location.latitude})"
curr.execute("""
INSERT INTO employee(firstname, familyname, city, road, building_nr,headqoters_id, rental_id, geo)
VALUES (
    ?,
    ?,
    ?,
    ?,
    ?,
    ?,
    ?,
    ST_GeomFromText(?, 4326)
)
""",(firstname, familyname,city,road,building_nr,headqoters_id,rental_id,point_wkt))


conn.commit()
conn.close()