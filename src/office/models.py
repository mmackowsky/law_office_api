from django.db import models


class Name(models.Model):
    first_name = models.CharField(max_length=100)
    surname = models.CharField(max_length=100)

    class Meta:
        abstract = True


class Speciality(models.Model):
    name = models.CharField(max_length=250)

    def __str__(self):
        return self.name


class Case(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()


class Lawyer(Name):
    speciality = models.ForeignKey(Speciality, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.first_name} {self.surname}"


class Client(Name):
    lawyer = models.ForeignKey(Lawyer, on_delete=models)
    case = models.ForeignKey(Case, on_delete=models)
