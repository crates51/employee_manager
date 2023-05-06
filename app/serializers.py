from datetime import datetime
from .models import Employee
from rest_framework import serializers
from django.contrib.auth.models import User


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ['url', 'username', 'email', 'groups']


class DateOfBirthField(serializers.DateField):
    # This is helping to serialize the data(e.g. into db)
    def to_representation(self, value):
        return value.strftime('%d/%m/%Y')

    # This is helping to deserialize the data(e.g. from db)
    def to_internal_value(self, value):
        try:
            # TODO: i thin i need to change the format in here
            return datetime.strptime(value, '%d/%m/%Y').date()
        except ValueError:
            raise serializers.ValidationError('Invalid date format. Please use DD/MM/YYYY format.')


class EmployeeSerializer(serializers.ModelSerializer):
    date_of_birth = DateOfBirthField()

    class Meta:
        model = Employee
        fields = '__all__'
