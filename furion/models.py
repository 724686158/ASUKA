from django.db import models
from furion.utils import AESCipher


class Uuev(models.Model):
    name = models.CharField(max_length=512, blank=False, db_index=True, )
    description = models.CharField(max_length=256)

    class Meta:
        abstract = True

    def __str__(self):
        return "{}[{}]".format(self.name, self.description)


class UuevProducer(Uuev):
    VALUE_TYPE = (
        ('STRING', 'string'),
        ('NOTSTR', 'notstring'),
    )
    is_secret = models.BooleanField(default=False)
    type = models.CharField(max_length=20, choices=VALUE_TYPE, default='STRING')
    value = models.CharField(max_length=512)

    def set_secret_value(self, secret_value):
        aes = AESCipher(self.name)
        self.value = aes.encrypt(secret_value)

    def get_secret_value(self):
        aes = AESCipher(self.name)
        return aes.decrypt(self.value)


class UuevConsumer(Uuev):
    SUPPORT_BY = (
        ('REGION', 'Region'),
        ('EXTERSEVER', 'ExternalService'),
        ('COMPONENT', 'Component'),
    )
    support_by = models.CharField(max_length=20, choices=SUPPORT_BY)
    supporter_name = models.CharField(max_length=128)
    uuev_name = models.CharField(max_length=512)


class Region(models.Model):
    name = models.CharField(max_length=50, primary_key=True)
    k8s_api_endpoint = models.CharField(max_length=128, blank=False, db_index=True)
    auth = models.CharField(max_length=512, blank=False)
    uuev_producers = models.ManyToManyField(UuevProducer)

    def __str__(self):
        return "{}".format(self.name)


class ExternalService(models.Model):
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
    uuev_producers = models.ManyToManyField(UuevProducer)

    def __str__(self):
        return "{}".format(self.name)



class Environment(models.Model):
    region = models.ForeignKey(Region)
    external_services = models.ManyToManyField(ExternalService)

