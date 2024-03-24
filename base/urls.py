from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('process_images/', views.process_images, name='process_images'),
     path('view_cleaned_json/', views.view_cleaned_json, name='view_cleaned_json'),
    path('model_qp/', views.model_qp, name='model_qp'),
    path('json-files/', views.json_files, name='json_files'),
    path('display-json-content/<str:filename>/', views.display_json_content, name='display_json_content'),
    path('model_qp_stored/<str:filename>/', views.model_qp_stored, name='model_qp_stored'),
    path('delete-all-data/', views.delete_all_data, name='delete_all_data'),

]
