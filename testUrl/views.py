from django.shortcuts import render
from django.http import HttpResponse
import sqlite3

def call_home(request):
    return render(request, 'home.html')

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
