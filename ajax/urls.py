from django.urls import path
from . import views as ajax_views

urlpatterns = [
    path('ajax_home/', ajax_views.ajax_home, name='ajax_home'),
    path('ajax_update/', ajax_views.ajax_update, name='ajax_update'),
    path('ajax_create/', ajax_views.ajax_create, name='ajax_create'),
    path('ajax_delete_by_id/<int:id>/', ajax_views.ajax_delete_by_id, name='ajax_delete_by_id'),
    path('ajax_call_view_edit/<int:id>/', ajax_views.ajax_call_view_edit, name='ajax_call_view_edit'),
    
]