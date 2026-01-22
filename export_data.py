from django.apps import apps
import os
import django
import json
from django.core import serializers

# Cấu hình môi trường Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mysite.settings')
django.setup()

# Xuất dữ liệu ra file với encoding utf-8
with open("data.json", "w", encoding="utf-8") as out:
    # Lấy tất cả các model ngoại trừ permission và contenttypes
    data = serializers.serialize("json", [obj for model in apps.get_models(
    ) for obj in model.objects.all() if model._meta.app_label not in ['auth', 'contenttypes']])
    out.write(data)

print("Xuất dữ liệu thành công vào file data.json!")
