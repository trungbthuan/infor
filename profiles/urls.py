from django.urls import path
from . import views as views


urlpatterns = [
    path('profiles_list/', views.profiles_list, name='profiles_list'),
    path('profiles_call_view_update/', views.profiles_call_view_update, name='profiles_call_view_update'),
    path('profiles_call_view_edit/<int:id>/', views.profiles_call_view_edit, name='profiles_call_view_edit'),
    path('profiles_update/<int:id>/', views.profile_update, name='profiles_update'),
    path('profiles_search_name/', views.profiles_search_name, name='profiles_search_name'),
    path('profiles_delete_by_id/<int:id>/', views.profiles_delete_by_id, name='profiles_delete_by_id'),
    path('profiles_call_profile_create/', views.call_profile_create, name='profiles_call_profile_create'),
    path('profiles_create/', views.profile_create, name='profiles_create'),
    # Sử dụng ModelForm
    # Tạo mới 1 nhân viên
    path('profile_ModelForm_create/', views.profile_ModelForm_create, name='profile_ModelForm_create'),
    # URL hiển thị Form nhập ID
    path('profile_get_by_id', views.profile_get_by_id, name='profile_get_by_id'),
    # URL xử lý việc lấy ID (POST) và làm trung gian chuyển hướng (REDIRECT)
    path('profile_find_redirect/', views.profile_find_redirect, name='profile_find_redirect'),
    # URL hiển thị Form EDIT (nhận ID qua URL/GET)
    path('profile_ModelForm_edit/<int:profile_id>/', views.profile_ModelForm_edit, name='profile_ModelForm_edit'),
    

]