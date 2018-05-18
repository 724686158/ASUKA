from django.db import models
from django.contrib.auth.models import User
import uuid


class UniversallyUniqueVariable(models.Model):
    url = models.CharField(max_length=512, blank=False, db_index=True, editable=False)

    class Meta:
        abstract = True

    def __str__(self):
        return "{}[{}]".format(self.name, self.description)


class AlchimestHook(models.Model):
    url = models.CharField(max_length=512, blank=False, primary_key=True)


class FurionHook(models.Model):
    url = models.CharField(max_length=512, blank=False, primary_key=True)


class History(models.Model):
    commit_id = models.UUIDField(primary_key=True, auto_created=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User)
    package_name = models.CharField(max_length=256)
    package_namespace = models.CharField(max_length=256)
    package_tag = models.CharField(max_length=50)
    environment_name = models.CharField(max_length=50)
    STATUS_TYPE = (
        ('PACKAGE_404', 'package 404 not found'),
        ('ENVIRONMENT_404', 'environment 404 not found'),
        ('ALCHIMEST_LOST', 'lost connect with alchimest'),
        ('FURION_LOST', 'lost connect with furion'),
        ('PACKAGE_ERROE', 'package has wrong variable declaration'),
        ('ENVIRONMENT_ERROR', 'environment has wrong variable declaration'),
        ('VARIABLE_NOT_MATCH', 'missing variable in the environment'),
        ('SUCCESS', 'success')
    )
    is_success = models.BooleanField(blank=False)
    result = models.FileField(upload_to='coil/')
    time = models.DateTimeField(auto_now_add=True)
