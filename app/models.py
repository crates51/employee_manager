from django.db import models


class Employee(models.Model):
    id = models.AutoField(primary_key=True)
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.EmailField(max_length=255, null=True)
    gender = models.CharField(max_length=1, null=True)
    date_of_birth = models.DateField()
    industry = models.CharField(max_length=255)
    salary = models.DecimalField(max_digits=10, decimal_places=2)
    years_of_experience = models.IntegerField()

    def __str__(self):
        return f"{self.first_name} {self.last_name}"
