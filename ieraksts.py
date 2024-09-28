import sqlite3
con=sqlite3.connect('Doktorats.db')
cur=con.cursor()
res=cur.execute("SELECT vaards, uzvaards FROM Pacienti;")
all=res.fetchall()
for row in all:
    print(row[0], row[1])
    print(row)