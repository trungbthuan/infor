from django.shortcuts import render
import sqlite3
from api.models import Profiles


def call_home(request):
    return render(request, 'home.html')


def dashboard(request):
    # 1. Đếm tổng số nhân viên
    total_staff = Profiles.objects.count()

    # 2. Đếm theo giới tính (Ví dụ: Nam)
    male_count = Profiles.objects.filter(sex='Nam').count()
    female_count = Profiles.objects.filter(sex='Nữ').count()

    # 3. Lấy 5 nhân viên mới vào làm gần đây nhất
    recent_staff = Profiles.objects.all().order_by('-recruitment_day')[:5]

    context = {
        'total_staff': total_staff,
        'male_count': male_count,
        'female_count': female_count,
        'recent_staff': recent_staff,
    }
    return render(request, 'dashboard.html', context)


def call_temp(request):
    return render(request, 'temp.html')


def call_temp2(request):
    return render(request, 'temp2.html')


def call_main(request):
    return render(request, "./main.html")


def get_students(request):
    conn = sqlite3.connect("db.sqlite3")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM 'api_students'")
    results = cursor.fetchall()
    conn.close()
    return render(request, './students.html', {'students': results})
