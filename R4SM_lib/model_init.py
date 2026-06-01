import sqlite3


conn = sqlite3.connect('R4SM_lib/data/Users.sqlite')
curr = conn.cursor()
curr.execute("CREATE TABLE users(login text, password text, familyname text, firstname text)")
curr.execute("""
    INSERT INTO users VALUES
        ('TestAdmin@test.com', 'Pass1234!', 'Test', 'Admin')
""")
conn.commit()
conn.close()

