from django.db import models
from django.contrib.auth.models import User
import uuid


class AlchimestHook(models.Model):
    url = models.CharField(max_length=512, blank=False, primary_key=True)


class FurionHook(models.Model):
    url = models.CharField(max_length=512, blank=False, primary_key=True)


class DeploymentRecord(models.Model):
    id = models.UUIDField(primary_key=True, auto_created=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User)
    package_name = models.CharField(max_length=256)
    package_namespace = models.CharField(max_length=256)
    package_tag = models.CharField(max_length=50)
    environment_name = models.CharField(max_length=50)
    is_success = models.BooleanField(blank=False)
    result = models.FileField(upload_to='coil/', null=True, blank=True, default=None)
    time = models.DateTimeField(auto_now_add=True)
