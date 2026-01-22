#!/usr/bin/env bash
# Lệnh tạo bảng
python manage.py migrate
# Lệnh nạp dữ liệu từ file json
python manage.py loaddata data.json