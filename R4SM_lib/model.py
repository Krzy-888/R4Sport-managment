import sqlite3
import regex as re

class user_model:
    def __init__(self,data_inputs:list[str],db:str = 'R4SM_lib/data/Users.sqlite'):
        login, password = data_inputs
        pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b'
        if re.fullmatch(pattern,login):
            conn = sqlite3.connect(db)
            curr = conn.cursor()
            res = curr.execute("SELECT * FROM users WHERE login=? AND password=?",(login,password))
            res = res.fetchall()
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
# TEST
user = user_model(['TestAdmin@test.com','Pass1234!'])
print(user.write_user_data())
# user = user_model(['TestAdmin','Pass1234!'])
# user = user_model(['TestAdmin@test.com','Pass1234'])