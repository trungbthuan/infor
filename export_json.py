import os
import django
from django.core.management import call_command

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mysite.settings')
django.setup()

# Xuất duy nhất bảng profiles của app api
with open('profiles_data.json', 'w', encoding='utf-8') as f:
    call_command(
        'dumpdata',
        'api.profiles',  # Tên_app.Tên_model
        stdout=f
    )

print("Đã xuất bảng api_profiles thành công vào file profiles_data.json!")
