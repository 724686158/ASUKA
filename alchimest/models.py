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
    JOB_TYPE = (
        ('RD', 'Research and Development'),
        ('OP', 'Operations'),
        ('QA', 'Quality Assurance'),
        ('PM', 'Product Manager'),
        ('SE', 'Software Engineer'),
    )
    job = models.CharField(max_length=40, choices=JOB_TYPE)
    own_namespaces = models.ManyToManyField(Namespace)

    def __str__(self):
        return "{}".format(self.user)


class GitLikeModel(models.Model):
    commit_id = models.UUIDField(primary_key=True, auto_created=True, default=uuid.uuid4, editable=False)
    namespace = models.ForeignKey(Namespace, blank=False)
    name = models.CharField(max_length=256, blank=False, db_index=True)
    tag = models.CharField(max_length=50, blank=False, default="")
    latest = models.BooleanField(default=True, editable=False)
    changed_from = models.UUIDField(default=None, null=True, blank=True, editable=False)

    class Meta:
        abstract = True
        unique_together = (("name", "namespace", "tag", ),)

    def __str__(self):
        if self.latest:
            return "[{}]{}:{}".format(self.namespace, self.name, self.tag) + "[NEW]"
        else:
            return "[{}]{}:{}".format(self.namespace, self.name, self.tag)

    def __unicode__(self):
        return self.__str__()


class Image(GitLikeModel):
    registry = models.CharField(max_length=256, blank=False)
    version = models.CharField(max_length=128, blank=False)

    def release_detail(self):
        return self.registry + ':' + self.version


class UniversallyUniqueVariable(models.Model):
    id = models.UUIDField(primary_key=True, auto_created=True, default=uuid.uuid4, editable=False)
    key = models.CharField(max_length=512, blank=False, db_index=True)
    VALUE_TYPE = (
        ('STRING', 'string'),
        ('NOTSTR', 'notstring'),
    )
    value_type = models.CharField(max_length=50, choices=VALUE_TYPE, default='STRING')
    VALUE_ORIGIN = (
        ('CURRENT', 'current'),
        ('REGION', 'region'),
        ('SERVICE', 'service'),
        ('CALCULATION', 'calculation'),
    )
    value_origin = models.CharField(max_length=50, choices=VALUE_ORIGIN, default='STRING')
    description = models.CharField(max_length=512, blank=False)
    value = models.CharField(max_length=512, blank=False)

    class Meta:
        unique_together = (("key", ),)

    def __str__(self):
        return "{}={}".format(self.key, self.value)


class Component(GitLikeModel):
    image = models.ForeignKey(Image, null=False)
    description = models.CharField(max_length=256, null=True,
                                   blank=True, default="")
    host_network = models.BooleanField(default=False)
    mem_per_instance = models.FloatField(default=128)
    cpu_per_instance = models.FloatField(default=0.125)
    use_uuvs = models.ManyToManyField(UniversallyUniqueVariable,
                                     through='UniversallyUniqueVariableInComponent',
                                     default=None)


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
    )
    type = models.CharField(max_length=50, choices=VALUE_TYPE, default='STRING')
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
    requests_storage_G = models.FloatField(default=1)
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

    description = models.CharField(max_length=256, blank=True,
                                   null=True, default="")
    approved = models.BooleanField(default=False)
    components = models.ManyToManyField(Component,
                                        through='ComponentRelease',
                                        default=None)
    use_uuvs = models.ManyToManyField(UniversallyUniqueVariable,
                                     through='UniversallyUniqueVariableInPackage',
                                     default=None)


class ComponentRelease(models.Model):
    component = models.ForeignKey(Component,
                                  related_name="deploy_comp",
                                  null=False, default=None)
    in_package = models.ForeignKey(Package,
                                   related_name="in_package",
                                   null=False, default=None)
    quantity = models.IntegerField(default=1, blank=False)
    description = models.CharField(max_length=256, blank=True,
                                   null=True, default="")
    examined = models.BooleanField(default=False)

    def __str__(self):
        return "{} in {}".format(self.component, self.in_package)


class UniversallyUniqueVariableInPackage(models.Model):
    uuv = models.ForeignKey(UniversallyUniqueVariable,
                                  related_name="use_this_uuv_in_package",
                                  null=False, default=None)
    in_package = models.ForeignKey(Package,
                                   related_name="uuv_in_this_package",
                                   null=False, default=None)


class UniversallyUniqueVariableInComponent(models.Model):
    uuv = models.ForeignKey(UniversallyUniqueVariable,
                                  related_name="use_this_uuv_in_component",
                                  null=False, default=None)
    in_component = models.ForeignKey(Component,
                                   related_name="uuv_in_this_component",
                                   null=False, default=None)

