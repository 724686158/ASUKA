# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Environment',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
            ],
        ),
        migrations.CreateModel(
            name='ExternalService',
            fields=[
                ('name', models.CharField(max_length=50, serialize=False, primary_key=True)),
                ('type', models.CharField(max_length=20, choices=[(b'REDIS', b'redis'), (b'MYSQL', b'mysql'), (b'MONGODB', b'mongodb'), (b'HBASE', b'hbase'), (b'OSS', b'oss'), (b'VIP', b'vip'), (b'DNS', b'dns'), (b'ELASTICSEARCH', b'elasticsearch'), (b'KAFKA', b'kafka'), (b'LB', b'lb'), (b'OTHERS', b'others')])),
            ],
        ),
        migrations.CreateModel(
            name='Region',
            fields=[
                ('name', models.CharField(max_length=50, serialize=False, primary_key=True)),
                ('k8s_api_endpoint', models.CharField(max_length=128, db_index=True)),
                ('auth', models.CharField(max_length=512)),
            ],
        ),
        migrations.CreateModel(
            name='UuevConsumer',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=512, db_index=True)),
                ('description', models.CharField(max_length=256)),
                ('support_by', models.CharField(max_length=20, choices=[(b'REGION', b'Region'), (b'EXTERSEVER', b'ExternalService'), (b'COMPONENT', b'Component')])),
                ('supporter_name', models.CharField(max_length=128)),
                ('uuev_name', models.CharField(max_length=512)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='UuevProducer',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=512, db_index=True)),
                ('description', models.CharField(max_length=256)),
                ('is_secret', models.BooleanField(default=False)),
                ('type', models.CharField(default=b'STRING', max_length=20, choices=[(b'STRING', b'string'), (b'NOTSTR', b'notstring')])),
                ('value', models.CharField(max_length=512)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.AddField(
            model_name='region',
            name='uuev_producers',
            field=models.ManyToManyField(to='furion.UuevProducer'),
        ),
        migrations.AddField(
            model_name='externalservice',
            name='uuev_producers',
            field=models.ManyToManyField(to='furion.UuevProducer'),
        ),
        migrations.AddField(
            model_name='environment',
            name='external_services',
            field=models.ManyToManyField(to='furion.ExternalService'),
        ),
        migrations.AddField(
            model_name='environment',
            name='region',
            field=models.ForeignKey(to='furion.Region'),
        ),
    ]
