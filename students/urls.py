from django.urls import path
from . import views as views


urlpatterns = [
    path('notification/', views.student_notification, name='notification'),
    # Tạo mới
    path('create/', views.student_post, name='create'),
    path('list/', views.student_list, name='list'),
    path('update/', views.student_update, name='update'),
    # Gọi form student-edit.html
    path('edit/<int:id>', views.student_edit, name='edit'),
    # Xóa ngay trên form student-update.html
    path('delete/<int:id>', views.student_delete_by_id, name='delete'),
    path('customConfirm/', views.customConfirm, name='customConfirm'),
    # Xử lý CẬP NHẬT khi người dùng gửi từ form student-edit.html
    path('put/<int:id>/', views.student_put_by_id, name='put'),
    path('do_anything/', views.do_anything_view, name='do_anything'), #Thử gọi Django
    path('callAnotherTemplate/', views.call_Another_Template, name='callAnotherTemplate'),
]


