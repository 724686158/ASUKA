# -*- coding: UTF-8 -*-
from django.db import models
from django.contrib.auth.models import User
import uuid


class Namespace(models.Model):
    name = models.CharField(max_length=256, db_index=True)

    class Meta:
        unique_together = ('name',)

    def __str__(self):
        return "{}".format(self.name)


class Employee(models.Model):
    user = models.OneToOneField(User)
    own_namespaces = models.ManyToManyField(Namespace)

    def __str__(self):
        return "{}".format(self.user)


class Image(models.Model):
    namespace = models.ForeignKey(Namespace)
    name = models.CharField(max_length=256, blank=False, db_index=True)
    version = models.CharField(max_length=128, blank=False)

    class Meta:
        unique_together = ('namespace', 'name', 'version')

    def __str__(self):
        return "{}:{}".format(self.name, self.version)


class GitLikeModel(models.Model):
    name = models.CharField(max_length=256, blank=False, db_index=True)
    latest = models.BooleanField(default=True, editable=False)
    commit_id = models.UUIDField(primary_key=True, auto_created=True, default=uuid.uuid4, editable=False)
    changed_from = models.UUIDField(default=None, null=True, blank=True, editable=False)
    tag = models.CharField(max_length=50, blank=True, default="")
    commit_time = models.DateTimeField(auto_now_add=True, blank=True)

    class Meta:
        abstract = True

    def __str__(self):
        return "{}[{}]".format(self.name, self.tag)


class Component(GitLikeModel):
    namespace = models.ForeignKey(Namespace, blank=False)
    image = models.ForeignKey(Image, null=False)
    description = models.CharField(max_length=256, null=True,
                                   blank=True, default="")
    host_network = models.BooleanField(default=False)
    mem_per_instance = models.FloatField(default=128)
    cpu_per_instance = models.FloatField(default=0.125)


class Port(models.Model):
    component = models.ForeignKey(Component,
                                  related_name="port_of_comp",
                                  null=False, default=None)
    name = models.CharField(max_length=128, default='port-')
    container_port = models.CharField(max_length=128, default='80')
    # host_port = models.CharField(max_length=128, default='/')
    PROTOCOL = (
        ('TCP', 'tcp'),
        ('UDP', 'udp'),
    )
    protocol = models.CharField(max_length=20, choices=PROTOCOL,
                                default='TCP')


class Environment(models.Model):
    component = models.ForeignKey(Component,
                                  related_name="env_of_comp",
                                  null=False, default=None)
    name = models.CharField(max_length=256, default='')
    VALUE_TYPE = (
        ('STRING', 'string'),
        ('NOTSTR', 'notstring'),
        ('UUEV', 'uuev'),
    )
    type = models.CharField(max_length=20, choices=VALUE_TYPE, default='STRING')
    value = models.CharField(max_length=256, default='')


class Volume(models.Model):
    component = models.ForeignKey(Component,
                                  related_name="vol_of_comp",
                                  null=False, default=None)
    pvc_name = models.CharField(max_length=128, default='vol-')
    container_path = models.CharField(max_length=128, default='/')
    MODE = (
        ('Read&Write', 'rw'),
        ('ReadOnly', 'ro'),
    )
    mode = models.CharField(max_length=20, choices=MODE,
                            default='Read&Write')
    TYPE = (
        ('EMPTY', 'emptyDir'),
        ('HOST', 'hostPath'),
        ('SECRET', 'secret'),
    )
    type = models.CharField(max_length=20, choices=TYPE,
                            default='EMPTY')


class Affinity(models.Model):
    component = models.ForeignKey(Component,
                                       related_name="affinity_from_component")
    to_component = models.ForeignKey(Component,
                                     related_name="affinity_to_component")
    TYPE = (
        ('Affinity', 'affinity'),
        ('Anti-Affinity', 'anti-affinity'),
    )
    type = models.CharField(max_length=20, choices=TYPE, default='Affinity')
    reason = models.CharField(max_length=256, blank=True,
                              null=True, default="")

    def __str__(self):
        return "[{}] has {} with [{}]".format(self.component,
                                              self.type,
                                              self.to_component)


class Package(GitLikeModel):
    namespace = models.ForeignKey(Namespace)
    components = models.ManyToManyField(Component,
                                        through='ComponentRelease',
                                        default=None)
    description = models.CharField(max_length=256, blank=True,
                                   null=True, default="")


class ComponentRelease(models.Model):
    component = models.ForeignKey(Component,
                                  related_name="deploy_comp",
                                  null=False, default=None)
    in_package = models.ForeignKey(Package,
                                   related_name="in_package",
                                   null=False, default=None)
    quantity = models.IntegerField(default=1, blank=False)

