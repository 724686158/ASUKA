from django.db import models
from furion.utils import AESCipher

# class UuevProducer(UniversallyUniqueVariable):
#     VALUE_TYPE = (
#         ('STRING', 'string'),
#         ('NOTSTR', 'notstring'),
#     )
#     is_secret = models.BooleanField(default=False)
#     type = models.CharField(max_length=20, choices=VALUE_TYPE, default='STRING')
#     value = models.CharField(max_length=512)
#
#     def set_secret_value(self, secret_value):
#         aes = AESCipher(self.name)
#         self.value = aes.encrypt(secret_value)
#
#     def get_secret_value(self):
#         aes = AESCipher(self.name)
#         return aes.decrypt(self.value)
#
#
# class UuevConsumer(UniversallyUniqueVariable):
#     SUPPORT_BY = (
#         ('REGION', 'Region'),
#         ('EXTERSEVER', 'ExternalService'),
#         ('COMPONENT', 'Component'),
#     )
#     support_by = models.CharField(max_length=20, choices=SUPPORT_BY)
#     supporter_name = models.CharField(max_length=128)
#     uuev_name = models.CharField(max_length=512)


class Service(models.Model):
    name = models.CharField(max_length=50, primary_key=True)
    SERVER_TYPE = (
        ('REDIS', 'redis'),
        ('MYSQL', 'mysql'),
        ('MONGODB', 'mongodb'),
        ('HBASE', 'hbase'),
        ('OSS', 'oss'),
        ('VIP', 'vip'),
        ('DNS', 'dns'),
        ('ELASTICSEARCH', 'elasticsearch'),
        ('KAFKA', 'kafka'),
        ('LB', 'lb'),
        ('OTHERS', 'others'),
    )
    type = models.CharField(max_length=20, choices=SERVER_TYPE)

    def __str__(self):
        return "{}".format(self.name)


class Variable(models.Model):
    in_service = models.ForeignKey(Service,
                                  related_name="var_of_serice",
                                  null=False, default=None)
    name = models.CharField(max_length=256, default='')
    VALUE_TYPE = (
        ('STRING', 'string'),
        ('NOTSTR', 'notstring'),
        ('UUV', 'universallyUniqueVariable'),
    )
    type = models.CharField(max_length=50, choices=VALUE_TYPE, default='STRING')
    value = models.CharField(max_length=256, default='')
    def __str__(self):
        return "{}".format(self.name)


class Region(models.Model):
    name = models.CharField(max_length=50, primary_key=True)
    k8s_api_endpoint = models.CharField(max_length=128, blank=False, db_index=True)
    auth_token = models.CharField(max_length=512, blank=False)

    def __str__(self):
        return "{}".format(self.name)


class Environment(models.Model):
    name = models.CharField(max_length=50, primary_key=True)
    region = models.ForeignKey(Region, blank=True, null=True)
    services = models.ManyToManyField(Service,
                                      through='UseService',
                                      default=None)
    def __str__(self):
        return "{}".format(self.name)


class UseService(models.Model):
    service = models.ForeignKey(Service,
                                  related_name="use_service",
                                  null=False, default=None)
    in_environment = models.ForeignKey(Environment,
                                   related_name="in_environment",
                                   null=False, default=None)
    exclusive = models.BooleanField(default=False)

    def __str__(self):
        return "{} in {}".format(self.service, self.in_environment)