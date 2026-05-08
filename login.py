import sqlite3

# INPUT
login = input()
password = input()

# LOGIC
# ('TestAdmin@test.com', 'Pass1234!')
conn = sqlite3.connect('data/Users.sqlite')
curr = conn.cursor()
res = curr.execute(f"SELECT * FROM users WHERE login='{login}' AND password='{password}'")
res = res.fetchall()

if res:
    access = True
else:
    access = False

# OUTPUT
print(access)