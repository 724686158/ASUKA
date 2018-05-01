# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('alchimest', '0002_auto_20180427_0917'),
    ]

    operations = [
        migrations.CreateModel(
            name='Environment',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(default=b'', max_length=256)),
                ('is_secret', models.BooleanField(default=False)),
                ('type', models.CharField(default=b'STRING', max_length=20, choices=[(b'STRING', b'string'), (b'NOTSTR', b'notstring'), (b'UUEV', b'uuev')])),
                ('value', models.CharField(default=b'', max_length=256)),
                ('component', models.ForeignKey(related_name='env_of_comp', default=None, to='alchimest.Component')),
            ],
        ),
        migrations.CreateModel(
            name='Volume',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('pvc_name', models.CharField(default=b'vol-', max_length=128)),
                ('container_path', models.CharField(default=b'/', max_length=128)),
                ('mode', models.CharField(default=b'Read&Write', max_length=20, choices=[(b'Read&Write', b'rw'), (b'ReadOnly', b'ro')])),
                ('type', models.CharField(default=b'EMPTY', max_length=20, choices=[(b'EMPTY', b'emptyDir'), (b'HOST', b'hostPath'), (b'SECRET', b'secret')])),
                ('component', models.ForeignKey(related_name='vol_of_comp', default=None, to='alchimest.Component')),
            ],
        ),
        migrations.RemoveField(
            model_name='environmentvariable',
            name='component',
        ),
        migrations.RemoveField(
            model_name='volumeclaim',
            name='component',
        ),
        migrations.DeleteModel(
            name='EnvironmentVariable',
        ),
        migrations.DeleteModel(
            name='VolumeClaim',
        ),
    ]
