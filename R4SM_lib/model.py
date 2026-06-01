import sqlite3
import regex as re
from geopy.geocoders import Nominatim

class user_model:
    def __init__(self,data_inputs:list[str],db:str = 'R4SM_lib/data/Users.sqlite'):
        login, password = data_inputs
        pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b'
        if re.fullmatch(pattern,login):
            conn = sqlite3.connect(db)
            curr = conn.cursor()
            res = curr.execute("SELECT * FROM users WHERE login=? AND password=?",(login,password))
            res = res.fetchall()
            conn.close()
            print(res)
            if res:
                self.mail = res[0][0]
                self.familyname = res[0][2]
                self.firstname = res[0][3]
            else:
                raise ValueError(f'Invalid email address or password')
        else:
            raise ValueError(f'Invalid email address')
    def write_user_data(self) -> list[str]:
        return [self.mail, self.familyname, self.firstname]

class R4SR4SDB_model:
    def __init__(self,db:str = 'R4SM_lib/data/R4SDB.sqlite'):
        self.conn = sqlite3.connect(db)
        self.conn.enable_load_extension(True)
        self.conn.load_extension(r"R4SM_lib/modules/mod_spatialite.dll")
        self.curr = self.conn.cursor()
        self.curr.execute("SELECT InitSpatialMetaData(1)")
        self.API = Nominatim(user_agent='App')
    def get_headquaters_list(self):
        res = self.curr.execute('SELECT id, name, city, road, building_nr,X(geo),Y(geo) FROM headquarters')
        self.headquaters_list = {}
        for r in res:
            self.headquaters_list[f'{r[1]} #{r[0]}'] = r[1:7]
        return self.headquaters_list
    def find_location(self,city,road,building_nr):
        address = f'{city}, {road} {building_nr}'
        try:
            location = self.API.geocode(address)
            point_wkt = f"POINT({location.longitude} {location.latitude})"
            return point_wkt
        except:
            try:
                location = self.API.geocode(city)
                point_wkt = f"POINT({location.longitude} {location.latitude})"
                return point_wkt
            except:
                return None
    
    def add_headquaters_list(self,input_data:list[str]):
        name,city,road,building_nr = input_data
        point_wkt = self.find_location(city,road,building_nr)
        if point_wkt:
            self.curr.execute("""
            INSERT INTO headquarters(name, city, road, building_nr, geo)
            VALUES (
                ?,
                ?,
                ?,
                ?,
                ST_GeomFromText(?, 4326)
            )
            """,(name,city,road,building_nr,point_wkt))
            self.conn.commit()
        else:
            raise ValueError(f'Invalid address')
    
    def remove_headquater(self, id_key:str):
        id = id_key.split('#')[-1]
        self.curr.execute("""
        DELETE FROM headquarters
        WHERE id = ?
        """, (id,))
        self.conn.commit()
    def update_headquater(self, id_key:str,input_data:list[str]):
        id = id_key.split('#')[-1]
        name,city,road,building_nr = input_data
        point_wkt = self.find_location(city,road,building_nr)
        if point_wkt:
            self.curr.execute("""
        UPDATE headquarters
        SET name = ?,
            city = ?,
            road = ?,
            building_nr = ?,
            geo = ST_GeomFromText(?, 4326)
        WHERE id = ?
    """, (name, city, road, building_nr, point_wkt, id))
            self.conn.commit()
        else:
            raise ValueError(f'Invalid address')


# TEST
# user = user_model(['TestAdmin@test.com','Pass1234!'])
# print(user.write_user_data())
# user = user_model(['TestAdmin','Pass1234!'])
# user = user_model(['TestAdmin@test.com','Pass1234'])
R4S = R4SR4SDB_model()
print(R4S.get_headquaters_list())
R4S.add_headquaters_list(['Rent 4 Sport','Łódź', 'Piotrkowska', '16'])
R4S.add_headquaters_list(['Rent 4 Sport','Łódź', '', ''])
print(R4S.get_headquaters_list())
# R4S.remove_headquater('Rent 4 Sport #4')
R4S.remove_headquater('Rent 4 Sport #2')
# R4S.remove_headquater('Rent 4 Sport #3')
print(R4S.get_headquaters_list())
R4S.update_headquater('Rent 4 Sport #3',['Rent 4 Sport','Kraków', '', ''])
print(R4S.get_headquaters_list())
R4S.remove_headquater('Rent 4 Sport #3')
print(R4S.get_headquaters_list())