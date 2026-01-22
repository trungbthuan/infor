import os
import sys
import django
from django.core.management import call_command

# Thiết lập môi trường Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mysite.settings')
django.setup()

# Mở file với định dạng utf-8 chuẩn
with open('data.json', 'w', encoding='utf-8') as f:
    # Gọi lệnh dumpdata trực tiếp từ code Python
    call_command(
        'dumpdata',
        exclude=['auth.permission', 'contenttypes', 'admin.logentry'],
        stdout=f
    )

print("Chúc mừng! Dữ liệu đã được xuất ra file data.json thành công với định dạng UTF-8.")
