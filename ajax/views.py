from datetime import datetime
import requests
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from api.forms import ProfileForm
from api.models import Profiles
from django.urls import reverse

#----------------------- Gọi form thêm mới nhân viên -------------------------------
def ajax_create(request):
    return render(request, 'ajax-create.html')

#-----------------------Hết phần gọi form thêm mới nhân viên -----------------------

#----------------------- Cập nhật thông tin từ view edit ---------------------------
def ajax_update(request, id):
    api_url = f'http://localhost:8080/api/profile/{id}/' 

    # --- Xử lý CẬP NHẬT DỮ LIỆU (Khi form được gửi: POST) ---
    if request.method == 'POST':
        
        # Lấy dữ liệu từ form gửi lên
        updated_data = {
            'full_name': request.POST.get('full_name'),
            'birthday': request.POST.get('birthday'), 
            'sex': request.POST.get('sex'),
            'birth_place': request.POST.get('birth_place'),
            'nation': request.POST.get('nation'),
            'recruitment_day': request.POST.get('recruitment_day'),
            'job_title': request.POST.get('job_title'),
            'department': request.POST.get('department'),
        }
        # Lọc bỏ các trường không cần thiết hoặc rỗng nếu bạn muốn sử dụng PATCH
        # (LƯU Ý: DRF serializer có thể tự lo việc này, nhưng lọc ở đây làm cho dữ liệu gửi đi sạch hơn)
        
        # 2. Xử lý xác thực (Gửi kèm Session Cookie)
        s = requests.Session()
        s.cookies.update(request.COOKIES) 
        
        # 3. LẤY CSRF TOKEN TỪ COOKIE VÀ THÊM VÀO HEADER
        # Lấy token từ cookie có tên 'csrftoken' (Django tự đặt)
        csrf_token = request.COOKIES.get('csrftoken')
        
        # Thêm token vào headers. Tên header phải là X-CSRFToken.
        headers = {
            'X-CSRFToken': csrf_token
        }

        # 4. Gửi yêu cầu PUT đến API
        # Truyền headers vào request
        response = s.put(api_url, data=updated_data, headers=headers)
        
        # Lưu ý: Khi dùng PUT, bạn cần đảm bảo updated_data phải chứa TẤT CẢ các trường.
        # Lưu ý: Khi dùng PATCH, bạn cần đảm bảo updated_data phải một số trường.
        # response = s.put(api_url, data=updated_data) 

        if response.status_code == 200:
            # Cập nhật thành công, chuyển hướng về trang danh sách
            return redirect('ajax_update') 
        else:
            # Xử lý lỗi từ API
            # Lấy chi tiết lỗi từ API
            error_details = response.json() if response.content else None
            context = {
                'Thông báo:': 'Đây là lỗ bạn càn sửa',
                'error_message': f'Cập nhật thất bại. Mã lỗi: {response.status_code}',
                'api_response': error_details,
                # 💥 SỬA: Truyền lại dữ liệu form dưới tên 'profile' để điền lại form HTML
                'profile': updated_data
            }
            # Trả lại form với thông báo lỗi
            return render(request, 'api/notification.html', {'message': context})
        
    # --- Xử lý HIỂN THỊ FORM (Khi form được yêu cầu: GET) ---
    else:
        # Tải dữ liệu sinh viên hiện tại để điền vào form
        s = requests.Session()
        s.cookies.update(request.COOKIES)
        
        response = s.get(api_url)
        
        if response.status_code == 200:
            profile = response.json()
            
            # Xử lý format ngày sinh cho input type="date" (phải là YYYY-MM-DD)
            try:
                # API trả về ngày tháng theo format "%Y-%m-%d" (ISO)
                datetime.strptime(profile['birthday'], "%Y-%m-%d") 
                datetime.strptime(profile['recruitment_day'], "%Y-%m-%d")
            except (ValueError, KeyError):
                # Nếu format sai, thiết lập giá trị rỗng hoặc xử lý lỗi
                profile['birthday'] = '' 
                
            return render(request, 'profile-edit.html', {'profile': profile})
        else:
            # Xử lý lỗi khi không tìm thấy sinh viên
            return HttpResponse(f"Không thể tải dữ liệu nhân viên. Mã lỗi: {response.status_code}", status=response.status_code)
#---------------------Hết phần update thông tin---------------------------

#----------------------- Gọi view edit  ---------------------------
def ajax_call_view_edit(request, id):
    api_url = f'http://localhost:8080/api/profile/{id}/'
    try:
        response = requests.get(api_url)
        if response.status_code == 200:
            profile = response.json()
            dt = datetime.strptime(profile['birthday'], "%d/%m/%Y")
            profile['birthday'] = dt.date()
            dt2 = datetime.strptime(profile['recruitment_day'], "%d/%m/%Y")
            profile['recruitment_day'] = dt2.date()
            return render(request, 'ajax-edit.html', {'profile': profile})
        else:
            error_message = f'Lỗi: Không thể lấy dữ liệu nhân viên. Mã trạng thái: {response.status_code}'
            return render(request, 'notification.html', {'message': error_message})
    except requests.exceptions.RequestException as e:
        error_message = f'Lỗi kết nối API: {e}'
        return render(request, 'notification.html', {'message': error_message})


def ajax_home(request):
    return render(request, 'ajax-home.html')

def ajax_update(request):
    return render(request, 'ajax-update.html')

def ajax_delete_by_id(request, id):
    api_url = f'http://localhost:8080/api/profile/{id}/' 
    if request.method == 'POST':
        s = requests.Session()
        s.cookies.update(request.COOKIES) 
        csrf_token = request.COOKIES.get('csrftoken')
            
        headers = {
        'X-CSRFToken': csrf_token
        }

        response = s.delete(api_url, headers=headers)
        
        if response.status_code == 204:
            # Xóa thành công, chuyển hướng về trang danh sách
            return redirect('ajax_update') 
        else: 
            error_details = response.json() if response.content else None
            context = {
                'Thông báo:': 'Đây là lỗ bạn càn sửa',
                'error_message': f'Cập nhật thất bại. Mã lỗi: {response.status_code}',
                'api_response': error_details,
            }
            return render(request, 'notification.html', {'message': context})
    else:
        return HttpResponse("Chương trình thực hiện không thành công", status=405)

