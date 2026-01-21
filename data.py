import sqlite3

# try:
#     conn = sqlite3.connect('db.sqlite3')
#     cursor = conn.cursor()
#     query = 'select * from auth_user;'
#     cursor.execute(query)
#     result = cursor.fetchall()
#     for row in result:
#         print('Username: ',format(row[4]), '; tên: ', format(row[5]))
#     cursor.close()
# except sqlite3.Error as error:
#     print('Error occurred - ', error)
# finally:
#     if conn:
#         conn.close()
#         print('SQLite Connection closed')

import requests

url = "http://localhost:8080/api/api-students/"

payload = {'id': '1807010189',
'full_name': 'Nguyễn Viết Toàn',
'birthday': '08/04/2000',
'sex': 'Nam',
'class_name': '5A-18',
'average': '3.61',
'morality': 'Tốt',
'performance': 'Giỏi'}
files=[

]
headers = {}

response = requests.request("POST", url, headers=headers, data=payload, files=files)

print(response.text)
