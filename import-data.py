import sqlite3
from datetime import datetime

conn = sqlite3.connect('db.sqlite3')
cursor = conn.cursor()

birthday = datetime.strptime('01/02/1997', '%d/%m/%Y').strftime('%Y-%m-%d')

cursor.execute(
    "UPDATE api_students SET birthday = ? WHERE id = ?", 
    (birthday, 1507010007)
)

conn.commit()
conn.close()
 	
 