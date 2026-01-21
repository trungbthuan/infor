from django.shortcuts import render, redirect
import requests
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
import json
from datetime import datetime
from django.contrib.auth.decorators import login_required

@require_http_methods(["GET"]) # Chỉ cho phép method GET
def do_anything_view(request):
    return JsonResponse({'message': 'Đã chạy lệnh Python trên server.'})

def call_Another_Template(request):
    return render(request, 'notification.html', {'message': 'Đã chạy lệnh Python trên server.'})

def student_notification(request):
    message="Test thử xem sao thôi mà"
    return render(request, 'notification.html', {'message': message} )

def customConfirm(request):
    return render(request, 'customConfirm.html')

def student_post(request):
    return render(request, 'student-post.html')

@login_required
def student_list(request):
    api_url = 'http://localhost:8080/api/api-list-students/'
    response = requests.get(api_url)
    students_data = response.json() 
    print(students_data)
    for student in students_data:
        dt = datetime.strptime(student['birthday'], "%d/%m/%Y")
        student['birthday'] = dt.date()
    
    return render(request, 'student-list.html', {'students': students_data})

@login_required
def student_update(request):
    api_url = 'http://localhost:8080/api/api-list-students/'
    
    try:
        response = requests.get(api_url, params=request.GET) 
        if response.status_code == 200:
            try:
                students_data = response.json() 
                for student in students_data:
                    dt = datetime.strptime(student['birthday'], "%d/%m/%Y")
                    student['birthday'] = dt.date()
            except requests.exceptions.JSONDecodeError:
                return render(request, 'notification.html', {'message': 'Lỗi: Phản hồi từ API không phải là JSON hợp lệ.'})
            return render(request, 'student-update.html', {'students': students_data})
        else:
            error_message = f'Lỗi: Không thể lấy dữ liệu sinh viên. Mã trạng thái: {response.status_code}'
            return render(request, 'notification.html', {'message': error_message})
    except requests.exceptions.RequestException as e:
        error_message = f'Lỗi kết nối API: {e}'
        return render(request, 'api/notification.html', {'message': error_message})

@login_required
def student_edit(request, id): # Gọi form student-edit.html
    api_url = f'http://localhost:8080/api/api-get-students-by-id/{id}/'
    try:
        response = requests.get(api_url)
        if response.status_code == 200:
            students_data = response.json()
            dt = datetime.strptime(students_data['birthday'], "%d/%m/%Y")
            students_data['birthday'] = dt.date()
            return render(request, 'student-edit.html', {'student': students_data})
        else:
            error_message = f'Lỗi: Không thể lấy dữ liệu sinh viên. Mã trạng thái: {response.status_code}'
            return render(request, 'notification.html', {'message': error_message})
    except requests.exceptions.RequestException as e:
        error_message = f'Lỗi kết nối API: {e}'
        return render(request, 'notification.html', {'message': error_message})

@login_required
def student_put_by_id(request, id): # Xử lý CẬP NHẬT khi người dùng gửi từ form student-edit.html

    api_url = f'http://localhost:8080/api/api-put-students/{id}/'
    
    if request.method == 'POST':
        # 2. Chuẩn bị dữ liệu từ form HTML (request.POST)
        data_request = request.POST.dict() 

        response = requests.put(api_url, data=data_request)

        if response.status_code in [200, 201]:
            return render(request, 'notification.html', {'message': f'Cập nhật sinh viên {id} thành công!'})
        else:
            try:
                error_json = response.json()
            except requests.exceptions.JSONDecodeError:
                error_json = {"detail": response.text}

            error_message = f'Cập nhật thất bại. Chi tiết: {json.dumps(error_json, ensure_ascii=False)}'
            return render(request, 'notification.html', {'message': error_message})

@login_required
def student_delete_by_id(request, id):
    api_url = f'http://localhost:8080/api/api-delete-students/{id}/'
    
    # 1. Gửi yêu cầu DELETE đến API (THAY vì requests.get)
    response = requests.delete(api_url) 
    
    # 2. Kiểm tra mã trạng thái thành công 204
    if response.status_code == 204:
        # Nếu xóa thành công, CHUYỂN HƯỚNG về trang danh sách/cập nhật
        return redirect('update') 
    else:
        error_message = f'Lỗi xóa sinh viên {id}. Mã trạng thái: {response.status_code}'
        
        # Nếu API trả về JSON lỗi, bạn có thể cố gắng đọc nó
        try:
            error_details = response.json()
            error_message += f' - Chi tiết: {error_details}'
        except:
            # Bỏ qua nếu không phải JSON
            pass
            
        return render(request, 'notification.html', {'message': error_message})
    
    

