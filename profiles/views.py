from datetime import datetime
import requests
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
import urllib.parse # Cần để mã hóa chuỗi tìm kiếm
from api.forms import ProfileForm
from api.models import Profiles
from django.urls import reverse


def call_home(request):
    return render(request, 'homePro.html')

def call_profile_create(request):
    return render(request, 'profile-create.html')

# Phần này sử dụng ModelForm-------------------------------------------------------------
# ---------------------------- Call profile_ModelForm_update ----------------------------
def profile_get_by_id(request):
    return render(request, 'profile-get-id.html')
# ----------------------- Tạo View Trung gian để tìm kiếm và Chuyển hướng ---------------
def profile_find_redirect(request):
    if request.method == 'POST':
        profile_id = request.POST.get('id')
        
        # 1. Kiểm tra ID có tồn tại không
        # Nếu không tồn tại, hàm get_object_or_404 sẽ tự động ném ra lỗi 404
        profile = get_object_or_404(Profiles, id=profile_id)
        
        # 2. CHUYỂN HƯỚNG SANG VIEW HIỂN THỊ FORM
        # Sử dụng reverse để tạo URL động
        return redirect(reverse('profile_ModelForm_edit', args=[profile.id]))
        
    # Xử lý nếu ai đó cố gắng truy cập bằng GET (nên là lỗi 405 Method Not Allowed hoặc chuyển hướng về trang nhập ID)
    return redirect('profile_get_by_id')
# ----------------Hết phần Tạo View Trung gian để tìm kiếm và Chuyển hướng ---------------

# ---------------------------- Sử dụng ModelForm update profile ----------------------------
def profile_ModelForm_edit(request, profile_id): 
    # Lấy đối tượng (DÙNG ID TỪ URL)
    profile = get_object_or_404(Profiles, id=profile_id)

    if request.method == 'POST':
        # Đây là lúc người dùng nhấn nút "Cập nhật" trên Form Edit
        form = ProfileForm(request.POST, instance=profile)
        
        if form.is_valid():
            form.save()
            # Thông báo thành công và chuyển hướng
            return redirect('profiles_list')
    
    else:
        # 💥 ĐÂY LÀ KHỐI CHẠY ĐẦU TIÊN KHI HIỂN THỊ FORM (GET request)
        # Form được khởi tạo với instance, dữ liệu cũ sẽ được điền sẵn
        form = ProfileForm(instance=profile)
        
    # Truyền dữ liệu sang template
    context = {
        'form': form,
        'profile': profile
    }
    return render(request, 'profile-ModelForm-edit.html', context)
# ----------------------------------Hết phần ModelForm update profile ----------------------

# ---------------------------------- Sử dụng ModelForm ------------------------------------
def profile_ModelForm_create(request):
    if request.method == 'POST':
        # 1. Gán dữ liệu POST vào Form
        form = ProfileForm(request.POST) 
        
        # 2. Kiểm tra dữ liệu có hợp lệ không (Validation)
        if form.is_valid():
            # 3. Lưu dữ liệu đã hợp lệ vào database
            # Hàm save() tự động tạo và lưu đối tượng Profile mới
            form.save() 
            
            # Chuyển hướng người dùng sau khi thành công
            return redirect('profiles_list') # Thay bằng tên URL list view của bạn
            
    else:
        # Tạo Form rỗng cho yêu cầu GET (hiển thị Form lần đầu)
        form = ProfileForm() 

    # Truyền Form object sang template
    context = {'form': form}
    return render(request, 'profile-ModelForm-create.html', context)
# -------------------------------- Kết thúc phần ModelForm ------------------------------
# Hết phần sử dụng ModelForm-------------------------------------------------------------

# Phần này học sử dụng ViewSet và Router ------------------------------------------------
#------------------- Phần create --------------------------------------
def profile_create(request):
    api_url = 'http://localhost:8080/api/profile/' 

    if request.method == 'POST':
        
        data_to_send = {
            'full_name': request.POST.get('full_name'),
            'birthday': request.POST.get('birthday'), 
            'sex': request.POST.get('sex'),
            'birth_place': request.POST.get('birth_place'),
            'nation': request.POST.get('nation'), 
            'recruitment_day': request.POST.get('recruitment_day'),
            'job_title': request.POST.get('job_title'),
            'department': request.POST.get('department'),
        }
        
        s = requests.Session()
        s.cookies.update(request.COOKIES) 
        csrf_token = request.COOKIES.get('csrftoken')
            
        headers = {
        'X-CSRFToken': csrf_token
        }
        
        response = s.post(api_url, data=data_to_send, headers=headers)

        if response.status_code == 201:
            return redirect('profiles_call_profile_create') # Chuyển hướng về trang danh sách
        else:
            # Tạo mới thất bại (Ví dụ: 400 Bad Request, 401 Unauthorized)
            # Lấy thông báo lỗi từ API
            error_details = {}
            try:
                error_details = response.json()
            except requests.exceptions.JSONDecodeError:
                error_details = {'non_field_errors': ['Lỗi không xác định từ API.']}
                
            context = {
                'errors': error_details,
                'form_data': data_to_send, # Giữ lại dữ liệu đã nhập
                'status_code': response.status_code
            }
            # Hiển thị lại form với thông báo lỗi
            return render(request, 'notification.html', {'message': context})
        
    else:
        # Lần đầu truy cập, hiển thị form trống
        return render(request, 'profile-create.html', {'profile': {}})

#------------------- Hết phần create ----------------------------------

#------------------- Phần delete --------------------------------------
def profiles_delete_by_id(request, id):
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
            return redirect('profiles_call_view_update') 
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
#-------------------Hết phần delete -----------------------------------


#-------------------Search name ---------------------------------------
def profiles_search_name(request):
    # 1. Lấy giá trị tìm kiếm từ Query String (request.GET)
    search_query = request.GET.get('search_fields', '') # Lấy giá trị từ input có name="search_fields"
    # 2. Mã hóa giá trị tìm kiếm để đảm bảo URL hợp lệ
    encoded_query = urllib.parse.quote_plus(search_query)
    # 3. Xây dựng API URL chính xác
    # Chú ý: DRF SearchFilter sử dụng tham số là 'search', không phải 'search_fields'
    api_url = f'http://localhost:8080/api/profile/?search={encoded_query}'

    if request.method == 'GET':
        s = requests.Session()
        s.cookies.update(request.COOKIES) 
        response = s.get(api_url)
        if response.status_code == 200:
            profiles = response.json()
            # --- Xử lý ngày tháng an toàn cho LIST ---
            processed_profiles = []
            for profile in profiles:
                try:
                    # Đảm bảo bạn đang xử lý list of objects
                    datetime.strptime(profile['birthday'], "%Y-%m-%d")
                    datetime.strptime(profile['recruitment_day'], "%Y-%m-%d")
                except (ValueError, KeyError, TypeError): 
                    # Xử lý lỗi nếu không tìm thấy key hoặc không phải dictionary
                    profile['birthday'] = ''
                processed_profiles.append(profile)
            return render(request, 'profiles-update.html', {'profiles': processed_profiles, 'search_query': search_query})
        else:
            return HttpResponse(f"Không thể tải dữ liệu. Mã lỗi: {response.status_code}", status=response.status_code)
    
    # Nếu không phải GET (chẳng hạn bạn muốn thêm xử lý POST/cách khác)
    return HttpResponse("Phương thức không hợp lệ", status=405)
                
#------------------ Hết phần search name ------------------------------

#------------------- Phần update --------------------------------------
def profile_update(request, id):
    # 1. Định nghĩa API Endpoint cho chi tiết (sử dụng pk)
    # URL: http://localhost:8080/api/students/{pk}/
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
            return redirect('profiles_call_view_update') 
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
            return render(request, 'notification.html', {'message': context})
        
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
#---------------------Hết profile update---------------------------



#---------------------Goi view profile edit -----------------------------
def profiles_call_view_edit(request, id):
    api_url = f'http://localhost:8080/api/profile/{id}/'
    try:
        response = requests.get(api_url)
        if response.status_code == 200:
            profile = response.json()
            dt = datetime.strptime(profile['birthday'], "%d/%m/%Y")
            profile['birthday'] = dt.date()
            dt2 = datetime.strptime(profile['recruitment_day'], "%d/%m/%Y")
            profile['recruitment_day'] = dt2.date()
            return render(request, 'profile-edit.html', {'profile': profile})
        else:
            error_message = f'Lỗi: Không thể lấy dữ liệu nhân viên. Mã trạng thái: {response.status_code}'
            return render(request, 'notification.html', {'message': error_message})
    except requests.exceptions.RequestException as e:
        error_message = f'Lỗi kết nối API: {e}'
        return render(request, 'notification.html', {'message': error_message})
#---------------------Hết phần profile edit---------------------------

#---------------------Goi view update -----------------------------       
def profiles_call_view_update(request):
    api_url = 'http://localhost:8080/api/profile/'
    try:
        # Sử dụng requests.Session để gửi kèm cookies (chứa session ID)
        s = requests.Session()
        s.cookies.update(request.COOKIES) 
        
        # Thực hiện request với Session
        response = s.get(api_url) 
        
    except requests.exceptions.ConnectionError:
        error_message = 'Lỗi kết nối API: Đảm bảo server API đang chạy (localhost:8080).'
        return render(request, 'notification.html', {'message': error_message})

    # 2. Xử lý Response
    if response.status_code == 200:
        profiles_data = response.json() 
        
        # Xử lý định dạng ngày sinh (Giữ nguyên như hàm cũ)
        for profile in profiles_data:
            # Giả sử Serializer vẫn trả về ngày tháng theo format "%d/%m/%Y"
            try:
                dt = datetime.strptime(profile['birthday'], "%d/%m/%Y")
                profile['birthday'] = dt.date()
                dt2 = datetime.strptime(profile['birth_place'], "%d/%m/%Y")
                profile['birth_place'] = dt2.date()
            except (ValueError, KeyError):
                # Xử lý nếu format bị lỗi hoặc trường 'birthday' không tồn tại
                pass
                
        return render(request, 'profiles-update.html', {'profiles': profiles_data})
        
    elif response.status_code == 401:
        # Nếu bị từ chối xác thực (401 Unauthorized)
        error_message = 'Lỗi: Bạn chưa đăng nhập. (401 Unauthorized).'
        # Bạn có thể chuyển hướng đến trang đăng nhập nếu cần
        # return redirect('login_url_name') 
        return render(request, 'notification.html', {'message': error_message}) 
        
    else:
        # Xử lý các lỗi khác
        error_message = f'Lỗi: Không thể lấy dữ liệu sinh viên. Mã trạng thái: {response.status_code}'
        return render(request, 'notification.html', {'message': error_message})


#---------------------Hết phần gọi view update

def profiles_list(request):
    # 1. URL MỚI: Dựa trên cấu hình Router
    # myapp/api/ + students/  =>  /api/students/
    api_url = 'http://localhost:8080/api/profile/' 
    
    # LƯU Ý QUAN TRỌNG: XỬ LÝ XÁC THỰC
    # Vì StudentViewSet của bạn dùng permission_classes = [IsAuthenticated],
    # Request này phải gửi kèm thông tin xác thực (ví dụ: Session Cookie).
    
    # Để request.get() hoạt động với Session Cookie (khi bạn đã đăng nhập)
    # bạn cần sử dụng một phiên (Session) của requests.
    try:
        # Sử dụng requests.Session để gửi kèm cookies (chứa session ID)
        s = requests.Session()
        s.cookies.update(request.COOKIES) 
        
        # Thực hiện request với Session
        response = s.get(api_url) 
        
    except requests.exceptions.ConnectionError:
        error_message = 'Lỗi kết nối API: Đảm bảo server API đang chạy (localhost:8080).'
        return render(request, 'notification.html', {'message': error_message})

    # 2. Xử lý Response
    if response.status_code == 200:
        profiles_data = response.json() 
        
        # Xử lý định dạng ngày sinh (Giữ nguyên như hàm cũ)
        for profile in profiles_data:
            # Giả sử Serializer vẫn trả về ngày tháng theo format "%d/%m/%Y"
            try:
                dt = datetime.strptime(profile['birthday'], "%d/%m/%Y")
                profile['birthday'] = dt.date()
                dt2 = datetime.strptime(profile['birth_place'], "%d/%m/%Y")
                profile['birth_place'] = dt2.date()
            except (ValueError, KeyError):
                # Xử lý nếu format bị lỗi hoặc trường 'birthday' không tồn tại
                pass
                
        return render(request, 'profiles-list.html', {'profiles': profiles_data})
        
    elif response.status_code == 401:
        # Nếu bị từ chối xác thực (401 Unauthorized)
        error_message = 'Lỗi: Bạn chưa đăng nhập. (401 Unauthorized).'
        # Bạn có thể chuyển hướng đến trang đăng nhập nếu cần
        # return redirect('login_url_name') 
        return render(request, 'notification.html', {'message': error_message}) 
        
    else:
        # Xử lý các lỗi khác
        error_message = f'Lỗi: Không thể lấy dữ liệu sinh viên. Mã trạng thái: {response.status_code}'
        return render(request, 'notification.html', {'message': error_message})
# Hết phần sử dụng ViewSet và Router ------------------------------------------------

