
from django.shortcuts import render, get_object_or_404, redirect
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status, viewsets
from rest_framework.permissions import AllowAny, IsAuthenticated
from api.models import Students, Profiles
from datetime import datetime
from .serializers import StudentsSerializer, ProfilesSerializer
import json
from rest_framework import filters
from .forms import ProfileForm
# Chỉ người dùng đã đăng nhập mới được thêm/sửa/xóa mới dùng IsAuthenticated 

# ---------------------------------- ViewSet và Router ------------------------------------
class ProfileViewSet(viewsets.ModelViewSet):
    # Chỉ định dữ liệu nguồn (tất cả sinh viên)
    queryset = Profiles.objects.all()
    # Chỉ định Serializer để xử lý dữ liệu
    serializer_class = ProfilesSerializer

    # Thêm SearchFilter
    filter_backends = [filters.SearchFilter] 

    # ❗ KHAI BÁO CÁC TRƯỜNG CHO PHÉP TÌM KIẾM
    # Mặc định, SearchFilter sử dụng tìm kiếm gần đúng (LIKE) và không phân biệt chữ hoa/thường.
    search_fields = ['full_name']  #, 'nation', 'job_title', 'department']

    # Chỉ định quyền truy cập (mặc định là AllowAny nếu bạn chưa có Auth)
    permission_classes = [AllowAny]


# ------------------------------ Kết thúc ViewSet và Router -------------------------------
@api_view(['GET'])
@permission_classes([AllowAny])
def first_api_view(request):
    if request.method == 'GET':
        return Response({'message': 'This is the API Home Page'}, status=status.HTTP_200_OK)

@api_view(['GET'])
@permission_classes([AllowAny])
def students_list(request):
    # Lấy tất cả đối tượng Model (QuerySet)
    students = Students.objects.all()
    # Khởi tạo Serializer:
    # many=True vì chúng ta đang xử lý một danh sách (nhiều đối tượng)
    serializer = StudentsSerializer(students, many=True)
    # Trả về dữ liệu đã được định dạng JSON tự động
    return Response(serializer.data)

@api_view(['POST'])
@permission_classes([IsAuthenticated]) # Chỉ người dùng đã đăng nhập mới được thêm
def students_create(request):
    
    # 1. Khởi tạo Serializer với dữ liệu gửi lên
    serializer = StudentsSerializer(data=request.data)
    
    if serializer.is_valid():
        # 2. LƯU VÀO DATABASE
        try:
            student = serializer.save()
            # 3. Trả về thông báo thành công
            return render(request, 'notification.html', {'message': 'Student created successfully'})
        
        except Exception as e:
            # Bẫy lỗi nếu có vấn đề gì xảy ra trong quá trình lưu (ví dụ: IntegrityError)
            error_message = f'Lỗi khi lưu vào Database: {e}'
            return render(request, 'notification.html', {'message': error_message})
            
    # Nếu chỉ muốn truyền lỗi dưới dạng chuỗi dễ đọc hơn:
    error_details = json.dumps(serializer.errors, indent=4, ensure_ascii=False)
    return render(request, 'notification.html', {'message': f'Dữ liệu gửi lên không hợp lệ: {error_details}'})

    # if request.method == 'POST':
    #     temp = datetime.strptime(request.POST.get('birthday'), '%d/%m/%Y')
    #     new_student = Students(
    #         full_name = request.POST.get('full_name'),
    #         birthday = temp.date(),
    #         sex = request.POST.get('sex'),
    #         class_name = request.POST.get('class_name'),
    #         average = request.POST.get('average'),
    #         morality = request.POST.get('morality'),
    #         performance = request.POST.get('performance')
    #     )
    #     new_student.save()
    # return render(request, 'notification.html', {'message': 'Student created successfully'})

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def students_get_all(request):
    search_name = request.GET.get('full_name', '')
    
    if search_name is None:
        students = Students.objects.all()
    else:
        students = Students.objects.all()
        students = students.filter(full_name__icontains=search_name)

    data=list(students.values())
    return render(request, 'student-update.html', {'students': data})

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def students_get_by_id(request, id):
    # Lấy 1 đối tượng Model
    student = get_object_or_404(Students, pk=id)
    # Khởi tạo Serializer: many=False (mặc định), vì chỉ có 1 đối tượng
    serializer = StudentsSerializer(student)
    # Trả về dữ liệu đã được định dạng JSON tự động
    return Response(serializer.data)
    # data = {
    #     'id': student.pk,
    #     'full_name': student.full_name, 
    #     'birthday': student.birthday.strftime("%d/%m/%Y"),
    #     'sex': student.sex,
    #     'class_name': student.class_name,
    #     'average': student.average,
    #     'morality': student.morality,
    #     'performance': student.performance,
    # }
    # return Response(data)

@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def students_delete(request, id):
    try:
        student = Students.objects.get(pk=id)
        # Xóa đối tượng
        student.delete() 
        # Trả về Response chuẩn: 204 No Content
        return Response(status=204) 
    except Students.DoesNotExist:
        # Trả về lỗi 404 nếu không tìm thấy sinh viên
        return Response({'error': 'Student not found'}, status=404)
    except Exception as e:
        # Xử lý các lỗi khác (ví dụ: lỗi database)
        return Response({'error': f'An error occurred during deletion: {e}'}, status=500)
    # student = get_object_or_404(Students, pk=id)
    # student.delete()
    # return render(request, 'notification.html', {'message': 'Cập nhật dữ liệu thành công'})

@api_view(['PUT', 'PATCH']) # Chấp nhận cả PUT (cập nhật toàn bộ) và PATCH (cập nhật một phần)
@permission_classes([IsAuthenticated])
def students_put(request, id):
    # 1. Lấy đối tượng sinh viên hiện tại bằng ID
    student = get_object_or_404(Students, pk=id)
    
    # 2. Khởi tạo Serializer:
    serializer = StudentsSerializer(instance=student, data=request.data, partial=True)
    
    # 3. XÁC THỰC DỮ LIỆU
    if serializer.is_valid():
        serializer.save()
        return render(request, 'notification.html', {'message': 'Cập nhậ dữ liệu thành công'})
    
    # 6. Nếu dữ liệu KHÔNG hợp lệ:
    error_details = json.dumps(serializer.errors, indent=4, ensure_ascii=False)
    return render(request, 'notification.html', {'message': f'Dữ liệu gửi lên không hợp lệ: {error_details}'})

# Ghi chú:
#     Lấy tất cả: Student.objects.all()
#     Lọc: Student.objects.filter(class_name='K60')
#     Lấy 1 đối tượng: Student.objects.get(pk=1)
#     Tạo mới: Student.objects.create(name='A', ...)