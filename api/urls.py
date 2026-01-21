from django.urls import path, include
from . import views as views
from .views import ProfileViewSet
from rest_framework.routers import DefaultRouter


# Khởi tạo Router
router = DefaultRouter()
# Đăng ký ViewSet của bạn với một URL prefix (tên đường dẫn)
# 'profile' sẽ là phần đầu của URL (ví dụ: /api/profile/)
router.register(r'profile', ProfileViewSet)
# Lệnh này tự động sinh ra 6 đường dẫn API chuẩn RESTful
# GET	/profile/	        list()	            Read (Đọc danh sách)
# POST	/profile/	        create()	        Create (Tạo mới)
# GET	/profile/{pk}/	    retrieve()	        Read (Đọc chi tiết)
# PUT	/profile/{pk}/	    update()	        Update (Cập nhật toàn bộ)
# PATCH	/profile/{pk}/	    partial_update()	Update (Cập nhật một phần)
# DELETE	/students/{pk}/	destroy()	        Delete (Xóa)
# Cấu hình URL patterns
urlpatterns = [
    # Router tự động tạo ra tất cả các URL (list, detail, create, update, delete)
    path('', include(router.urls)),
    # Lấy toàn bộ danh sách
    path('api-list-students/', views.students_list, name='api-list-students'), 
    # Tạo mới
    path('api-create-students/', views.students_create, name='api-create-students'),
    # Lấy một số students có tên giống nhau
    path('api-get-students-all/', views.students_get_all, name='api-get-students-all'),
    # Lây thông tin student them id
    path('api-get-students-by-id/<int:id>/', views.students_get_by_id, name='api-get-students-by-id'),
    # Cập nhật thông tin
    path('api-put-students/<int:id>/', views.students_put, name='api-put-students'),
    # URL Xóa thông tin bằng ID)
    path('api-delete-students/<int:id>/', views.students_delete, name='api-delete-students'),
]
