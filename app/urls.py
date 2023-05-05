from django.urls import path
from .views import EmployeeList, EmployeeDetail

urlpatterns = [
    path('', EmployeeList.as_view(), name='employee_list'),
    path('<int:pk>/', EmployeeDetail.as_view(), name='employee_detail'),
]
