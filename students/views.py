from django.shortcuts import render, redirect
import requests
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
import json
from datetime import datetime
from django.contrib.auth.decorators import login_required
from api.views import students_list, students_get_by_id, students_put, students_delete


@require_http_methods(["GET"])  # Chỉ cho phép method GET
def do_anything_view(request):
    return JsonResponse({'message': 'Đã chạy lệnh Python trên server.'})


def call_Another_Template(request):
    return render(request, 'notification.html', {'message': 'Đã chạy lệnh Python trên server.'})


def student_notification(request):
    message = "Test thử xem sao thôi mà"
    return render(request, 'notification.html', {'message': message})


def customConfirm(request):
    return render(request, 'customConfirm.html')


def student_post(request):
    return render(request, 'student-post.html')


@login_required
def student_list(request):
    # api_url = 'http://localhost:8080/api/api-list-students/'
    # Gọi trực tiếp hàm view API, không dùng requests.get(url)
    response = students_list(request)
    students_data = response.data
    # print(students_data)
    for student in students_data:
        dt = datetime.strptime(student['birthday'], "%d/%m/%Y")
        student['birthday'] = dt.date()

    return render(request, 'student-list.html', {'students': students_data})


@login_required
def student_update(request):
    # api_url = 'http://localhost:8080/api/api-list-students/'
    try:
        # 1. Chúng ta truyền chính object 'request' vào để hàm API lấy được params (request.GET)
        response = students_list(request)

        # 2. Kiểm tra mã trạng thái trả về từ DRF Response
        if response.status_code == 200:
            # Lấy dữ liệu từ thuộc tính .data (DRF) thay vì .json()
            students_data = response.data

            # 3. Xử lý định dạng ngày tháng
            for student in students_data:
                # Kiểm tra nếu birthday là chuỗi thì mới parse,
                # vì đôi khi gọi nội bộ dữ liệu có thể đã là object date
                if isinstance(student.get('birthday'), str):
                    try:
                        dt = datetime.strptime(student['birthday'], "%d/%m/%Y")
                        student['birthday'] = dt.date()
                    except (ValueError, KeyError):
                        pass

            return render(request, 'student-update.html', {'students': students_data})

        else:
            error_message = f'Lỗi: Không thể lấy dữ liệu sinh viên. Mã trạng thái: {response.status_code}'
            return render(request, 'notification.html', {'message': error_message})

    except Exception as e:
        # Bắt các lỗi logic hoặc lỗi import
        error_message = f'Lỗi hệ thống khi truy vấn dữ liệu: {str(e)}'
        return render(request, 'notification.html', {'message': error_message})


@login_required
def student_edit(request, id):  # Gọi form student-edit.html
    # api_url = f'http://localhost:8080/api/api-get-students-by-id/{id}/'
    try:
        response = students_get_by_id(request, id)
        # response = requests.get(api_url)
        if response.status_code == 200:
            students_data = response.data
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
def student_put_by_id(request, id):

    # api_url = f'http://localhost:8080/api/api-put-students/{id}/'
    if request.method == 'POST':

        request.method = 'PUT'  # Thay đổi method thành PUT
        # Gọi trực tiếp hàm view API, không dùng requests.put(url)
        try:
            response = students_put(request, id)
            # 3. Xử lý kết quả trả về (Response từ DRF)
            if response.status_code in [200, 204]:
                return render(request, 'notification.html', {
                    'message': f'Cập nhật sinh viên {id} thành công!'
                })
            else:
                # Lấy dữ liệu lỗi từ response.data (DRF trả về .data thay vì .json())
                error_details = response.data
                error_message = f'Cập nhật thất bại (Mã {response.status_code}). Chi tiết: {error_details}'
                return render(request, 'notification.html', {'message': error_message})
        except Exception as e:
            return render(request, 'notification.html', {'message': f'Lỗi hệ thống: {str(e)}'})
    # Nếu là GET hoặc phương thức khác
    return render(request, 'notification.html', {'message': f'Lỗi hệ thống: {id}'})


@login_required
def student_delete_by_id(request, id):
    # api_url = f'http://localhost:8080/api/api-delete-students/{id}/'
    # 1. Gửi yêu cầu DELETE đến API (THAY vì requests.get)
    request.method = 'DELETE'
    try:
        # 2. Gọi trực tiếp hàm View API, không dùng requests qua HTTP
        response = students_delete(request, id)

        # 3. Kiểm tra mã trạng thái thành công (DRF thường trả về 204 No Content khi xóa)
        if response.status_code in [204, 200]:
            # Nếu xóa thành công, chuyển hướng về trang danh sách
            return redirect('update')
        else:
            # Lấy chi tiết lỗi từ response.data
            error_details = getattr(response, 'data', 'Không có chi tiết lỗi')
            error_message = f'Lỗi xóa sinh viên {id}. Mã trạng thái: {response.status_code} - Chi tiết: {error_details}'
            return render(request, 'notification.html', {'message': error_message})

    except Exception as e:
        # Xử lý các lỗi phát sinh trong quá trình gọi hàm
        return render(request, 'notification.html', {'message': f'Lỗi hệ thống: {str(e)}'})
