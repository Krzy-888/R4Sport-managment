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
    # Init
    def __init__(self,db:str = 'R4SM_lib/data/R4SDB.sqlite'):
        self.conn = sqlite3.connect(db)
        self.conn.enable_load_extension(True)
        self.conn.load_extension(r"R4SM_lib/modules/mod_spatialite.dll")
        self.curr = self.conn.cursor()
        self.curr.execute("SELECT InitSpatialMetaData(1)")
        self.API = Nominatim(user_agent='App')
    
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
    # Headquaters
    def get_headquaters_list(self):
        res = self.curr.execute("""SELECT id, name, city,
                                road, building_nr,X(geo),Y(geo) 
                                FROM headquarters""").fetchall()
        self.headquaters_list = {}
        for r in res:
            self.headquaters_list[f'{r[1]} #{r[0]}'] = list(r[1:7])
        return self.headquaters_list
    
    def get_filtred_headquaters_list(self,filter:str,value):
        res = self.curr.execute(f"""SELECT id, name, city,
                                road, building_nr,X(geo),Y(geo) 
                                FROM headquarters
                                WHERE {filter} LIKE ?""",(value,)).fetchall()
        self.headquaters_list = {}
        for r in res:
            self.headquaters_list[f'{r[1]} #{r[0]}'] = list(r[1:7])
        return self.headquaters_list


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
    
    # Rental
    def get_rental_list(self):
        res = self.curr.execute("""SELECT id, name, city,
                                road, building_nr,X(geo),Y(geo),headqoters_id 
                                FROM rental""").fetchall()
        self.rental_list = {}
        for r in res:
            headquarters = self.curr.execute("""SELECT X(geo),Y(geo), name
                                FROM headquarters WHERE id = ?""",(r[7],)).fetchone()
            distance = self.curr.execute("""SELECT ST_Distance(
                                MakePoint(?, ?, 4326),
                                MakePoint(?, ?, 4326),
                                1
                                ) AS distance_m;""",(headquarters[0],headquarters[1],r[5],r[6])).fetchone()[0]
            self.rental_list[f'{r[1]} #{r[0]}'] = list(r[1:7])
            self.rental_list[f'{r[1]} #{r[0]}'].append(f'{headquarters[2]} #{r[7]}')
            self.rental_list[f'{r[1]} #{r[0]}'].append(round(distance/1000,2))
        return self.rental_list
    
    def get_filtred_rental_list(self,filter:str,value):
        res = self.curr.execute(f"""SELECT id, name, city,
                                road, building_nr,X(geo),Y(geo),headqoters_id 
                                FROM rental WHERE {filter} LIKE ?""",(value,)).fetchall()
        self.rental_list = {}
        for r in res:
            headquarters = self.curr.execute("""SELECT X(geo),Y(geo), name
                                FROM headquarters WHERE id = ?""",(r[7],)).fetchone()
            distance = self.curr.execute("""SELECT ST_Distance(
                                MakePoint(?, ?, 4326),
                                MakePoint(?, ?, 4326),
                                1
                                ) AS distance_m;""",(headquarters[0],headquarters[1],r[5],r[6])).fetchone()[0]
            self.rental_list[f'{r[1]} #{r[0]}'] = list(r[1:8])
            self.rental_list[f'{r[1]} #{r[0]}'].append(f'{headquarters[2]} #{r[7]}')
            self.rental_list[f'{r[1]} #{r[0]}'].append(round(distance/1000,2))
        return self.rental_list
    
    def add_rental_list(self,input_data:list):
        name,city,road,building_nr,headqoters_id = input_data
        point_wkt = self.find_location(city,road,building_nr)
        if point_wkt:
            self.curr.execute("""
            INSERT INTO rental(name, city, road, building_nr, headqoters_id, geo)
            VALUES (
                ?,
                ?,
                ?,
                ?,
                ?,
                ST_GeomFromText(?, 4326)
            )
            """,(name,city,road,building_nr,headqoters_id,point_wkt))
            self.conn.commit()
        else:
            raise ValueError(f'Invalid address')
        
    def remove_rental(self, id_key:str):
        id = id_key.split('#')[-1]
        self.curr.execute("""
        DELETE FROM rental
        WHERE id = ?
        """, (id,))
        self.conn.commit()

    def update_rental(self, id_key:str,input_data:list):
        id = id_key.split('#')[-1]
        name,city,road,building_nr,headqoters_id = input_data
        point_wkt = self.find_location(city,road,building_nr)
        if point_wkt:
            self.curr.execute("""
        UPDATE rental
        SET name = ?,
            city = ?,
            road = ?,
            building_nr = ?,
            headqoters_id = ?,
            geo = ST_GeomFromText(?, 4326)
        WHERE id = ?
    """, (name, city, road, building_nr, headqoters_id, point_wkt, id))
            self.conn.commit()
        else:
            raise ValueError(f'Invalid address')
        
    # Employee
    def get_employee_list(self):
        res = self.curr.execute("""SELECT id, firstname, familyname, city,
                                road, building_nr,X(geo),Y(geo),headqoters_id, rental_id 
                                FROM employee""").fetchall()
        self.employee_list = {}
        for r in res:
            rental = self.curr.execute("""SELECT X(geo),Y(geo), name
                                FROM rental WHERE id = ?""",(r[9],)).fetchone()
            headquarters = self.curr.execute("""SELECT  name
                                FROM headquarters WHERE id = ?""",(r[8],)).fetchone()
            distance = self.curr.execute("""SELECT ST_Distance(
                                MakePoint(?, ?, 4326),
                                MakePoint(?, ?, 4326),
                                1
                                ) AS distance_m;""",(rental[0],rental[1],r[6],r[7])).fetchone()[0]
            self.employee_list[f'{r[1]} {r[2]} #{r[0]}'] = list(r[1:8])
            self.employee_list[f'{r[1]} {r[2]} #{r[0]}'].append(f'{headquarters[0]} #{r[8]}')
            self.employee_list[f'{r[1]} {r[2]} #{r[0]}'].append(f'{rental[2]} #{r[9]}')
            self.employee_list[f'{r[1]} {r[2]} #{r[0]}'].append(round(distance/1000,2))
        return self.employee_list
    
    def get_filtred_employee_list(self, filter:str,value):
        res = self.curr.execute(f"""SELECT id, firstname, familyname, city,
                                road, building_nr,X(geo),Y(geo),headqoters_id, rental_id 
                                FROM employee WHERE {filter} LIKE ?""",(value,)).fetchall()
        self.employee_list = {}
        for r in res:
            rental = self.curr.execute("""SELECT X(geo),Y(geo),name
                                FROM rental WHERE id = ?""",(r[9],)).fetchone()
            headquarters = self.curr.execute("""SELECT  name
                                FROM headquarters WHERE id = ?""",(r[8],)).fetchone()
            distance = self.curr.execute("""SELECT ST_Distance(
                                MakePoint(?, ?, 4326),
                                MakePoint(?, ?, 4326),
                                1
                                ) AS distance_m;""",(rental[0],rental[1],r[6],r[7])).fetchone()[0]
            self.employee_list[f'{r[1]} {r[2]} #{r[0]}'] = list(r[1:8])
            self.employee_list[f'{r[1]} {r[2]} #{r[0]}'].append(f'{headquarters[0]} #{r[8]}')
            self.employee_list[f'{r[1]} {r[2]} #{r[0]}'].append(f'{rental[2]} #{r[9]}')
            self.employee_list[f'{r[1]} {r[2]} #{r[0]}'].append(round(distance/1000,2))
        return self.employee_list

    def add_employee_list(self,input_data:list):
        firstname, familyname,city,road,building_nr,rental_id = input_data
        headqoters_id = self.curr.execute(""" SELECT headqoters_id
                                FROM rental WHERE id = ?""",(rental_id,)).fetchone()[0]
        point_wkt = self.find_location(city,road,building_nr)
        if point_wkt:
            self.curr.execute("""
            INSERT INTO employee(firstname, familyname, city, road, building_nr, headqoters_id, rental_id, geo)
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
            """,(firstname, familyname,city,road,building_nr,headqoters_id,rental_id ,point_wkt))
            self.conn.commit()
        else:
            raise ValueError(f'Invalid address')
        
    def remove_employee(self, id_key:str):
        id = id_key.split('#')[-1]
        self.curr.execute("""
        DELETE FROM employee
        WHERE id = ?
        """, (id,))
        self.conn.commit()

    def update_employee(self, id_key:str,input_data:list):
        id = id_key.split('#')[-1]
        firstname, familyname,city,road,building_nr,rental_id = input_data
        point_wkt = self.find_location(city,road,building_nr)
        headqoters_id = self.curr.execute(""" SELECT headqoters_id
                                FROM rental WHERE id = ?""",(rental_id,)).fetchone()[0]
        if point_wkt:
            self.curr.execute("""
        UPDATE employee
        SET firstname = ?,
            familyname = ?,
            city = ?,
            road = ?,
            building_nr = ?,
            rental_id = ?,
            headqoters_id = ?,
            geo = ST_GeomFromText(?, 4326)
        WHERE id = ?
    """, (firstname, familyname, city, road, building_nr, headqoters_id,rental_id, point_wkt, id))
            self.conn.commit()
        else:
            raise ValueError(f'Invalid address')
# TEST
if __name__ == '__main__':
    # user = user_model(['TestAdmin@test.com','Pass1234!'])
    # print(user.write_user_data())
    # user = user_model(['TestAdmin','Pass1234!'])
    # user = user_model(['TestAdmin@test.com','Pass1234'])
    R4S = R4SR4SDB_model()
    # print(R4S.get_headquaters_list())
    # R4S.add_headquaters_list(['Rent 4 Sport','Łódź', 'Piotrkowska', '16'])
    # R4S.add_headquaters_list(['Rent 4 Sport','Łódź', '', ''])
    # print(R4S.get_headquaters_list())
    # # R4S.remove_headquater('Rent 4 Sport #4')
    # R4S.remove_headquater('Rent 4 Sport #2')
    # # R4S.remove_headquater('Rent 4 Sport #3')
    # print(R4S.get_headquaters_list())
    # R4S.update_headquater('Rent 4 Sport #3',['Rent 4 Sport','Kraków', '', ''])
    # print(R4S.get_headquaters_list())
    # R4S.remove_headquater('Rent 4 Sport #3')
    # print(R4S.get_headquaters_list())
    # print(R4S.get_rental_list())
    # R4S.add_rental_list(['Rent 4 Sport','Łódź', 'Piotrkowska', '16', 1])
    # print(R4S.get_rental_list())
    # R4S.update_rental('Rent 4 Sport #2',['Rent 4 Sport','Warszawa', 'Okopowa', '1', 1])
    # print(R4S.get_rental_list())
    # R4S.remove_rental('Rent 4 Sport #2')
    # print(R4S.get_rental_list())
    # R4S.add_headquaters_list(['Decathlon','Łódź', 'Piotrkowska', '16'])
    # R4S.add_rental_list(['Decathlon','Warszawa', 'Aleja Krakowska', '81', 2])
    # print(R4S.get_headquaters_list())
    # print(R4S.get_rental_list())
    # # print(R4S.get_rental_list_based_on_headquater(2))
    # # R4S.remove_headquater('Decathlon #2')
    # # R4S.remove_rental('Decathlon #2')
    # print(R4S.get_employee_list())
    # R4S.add_employee_list(['Bartosz', 'Łukasik','Warszawa','Kolska','5',1])
    # print(R4S.get_employee_list())
    # R4S.update_employee('Bartosz Łukasik #2',['Barbara', 'Łukasik','Warszawa','Kolska','5',1])
    # print(R4S.get_employee_list())
    # R4S.remove_employee('Barbara Łukasik #2')
    # print(R4S.get_filtred_employee_list('id',1))
    # print(R4S.get_employee_list())
    # print(R4S.get_filtred_employee_list('id','2'))

    R4S.conn.close()