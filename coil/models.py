from django.db import models

# Create your models here.
class A(models.Model):
    name = models.CharField(max_length=20)


class B(models.Model):
    name = models.CharField(max_length=20)
    a = models.ForeignKey(A)

