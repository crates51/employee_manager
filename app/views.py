import json
import datetime
import pandas as pd
from rest_framework import permissions, status, viewsets
from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib.auth.models import User
from django.core.paginator import Paginator
from django.http import Http404, JsonResponse
from .models import Employee
from .serializers import EmployeeSerializer, UserSerializer


class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]


class EmployeeList(APIView):
    # add permission to check if user is authenticated
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, *args, **kwargs):
        '''List all the Employees'''
        employees = Employee.objects.all()

        filter = request.GET.get('filter')
        sort_by = request.GET.get('sort_by')
        statistics = request.GET.get('statistics')
        page_number = request.GET.get('page_nr', 1)
        page_size = request.GET.get('page_size', 5)
        if filter:
            employees = filter_data(employees, filter)
        if sort_by:
            employees = employees.order_by(sort_by).values()
        paginator = Paginator(employees, page_size)
        page_obj = paginator.get_page(page_number)
        serializer = EmployeeSerializer(page_obj, many=True)
        if statistics:  # Getting statistics from the "final version" of the response
            return Response(get_statistics(serializer.data, statistics), status=status.HTTP_200_OK)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        '''Create a new Employee'''
        data = {
            'first_name': request.data.get('first_name'),
            'last_name': request.data.get('last_name'),
            'gender': request.data.get('gender'),
            'date_of_birth': request.data.get('date_of_birth'),
            'industry': request.data.get('industry'),
            'salary': request.data.get('salary'),
            'years_of_experience': request.data.get('years_of_experience'),
        }
        serializer = EmployeeSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class EmployeeDetail(APIView):
    # add permission to check if user is authenticated
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self, pk):
        '''Helper method for handling errors'''
        try:
            return Employee.objects.get(pk=pk)
        except Employee.DoesNotExist:
            raise Http404

    def get(self, request, pk):
        '''Get employee by key'''
        employee = self.get_object(pk)
        serializer = EmployeeSerializer(employee)
        return Response(serializer.data)

    def delete(self, request, pk):
        '''Delete employee by key'''
        employee = self.get_object(pk)
        employee.delete()
        return JsonResponse({"message": "Employee deleted successfully."})

    def put(self, request, pk):
        '''Update employee by key'''
        employee = self.get_object(pk)
        serializer = EmployeeSerializer(employee, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


def filter_data(employees, filter):
    '''
    Basic filter for employees.
    Filter parameter has to be of this form {"field": "value"}; e.g. {"first_name": "Leupold"}
    '''
    filter_kwargs = json.loads(filter)
    return employees.filter(**filter_kwargs)


def get_statistics(data, statistics):
    '''
    Gettings statistics based on the filtered result.
    Available statistics:
        AVERAGE_AGE_PER_INDUSTRY = 'Average age per industry'
        AVERAGE_SALARIES_PER_INDUSTRY = 'Average salaries per industry'
        AVERAGE_SALARIES_PER_YOE = 'Average salaries per years of experience'
        TODO: add some more
    Note: Because i did't undrestand the task clearly i used pandas directly on the database Data.
    What i would normally do to take these statistics is to create sql query which will directly
    calculate this statistics inside DB.
    '''

    result = {}
    records = pd.DataFrame.from_records(data)
    records = records[~records["industry"].str.contains("n/a")]  # Clean the industry rows
    if statistics == 'AVERAGE_AGE_PER_INDUSTRY':
        records['age'] = records['date_of_birth'].apply(calculate_age)
        result = records.groupby('industry')['age'].mean().round().astype(int).reset_index().to_dict('records')
    elif statistics == 'AVERAGE_SALARIES_PER_INDUSTRY':
        result = records.groupby('industry')['salary'].mean().reset_index().to_dict('records')
    elif statistics == 'AVERAGE_SALARIES_PER_YOE':
        result = records.groupby('years_of_experience')['salary'].mean().round().astype(int).reset_index().to_dict('records')
    return result


def calculate_age(born):
    born = datetime.datetime.strptime(born, "%d/%m/%Y")
    today = datetime.date.today()
    age = today.year - born.year - ((today.month, today.day) < (born.month, born.day))
    return age
