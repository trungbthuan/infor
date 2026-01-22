import sqlite3

# Kết nối đến file database SQLite của bạn
conn = sqlite3.connect('db.sqlite3')
file_path = 'profiles_data.sql'

with open(file_path, 'w', encoding='utf-8') as f:
    # Lệnh .dump của SQLite để xuất toàn bộ cấu trúc và dữ liệu
    # Ở đây chúng ta lọc riêng bảng api_profiles
    for line in conn.iterdump():
        if 'api_students' in line:
            f.write('%s\n' % line)

conn.close()
print(
    f"Thành công! Dữ liệu bảng api_profiles đã được ghi vào file {file_path}")
