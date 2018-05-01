# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings
import uuid


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Affinity',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('type', models.CharField(default=b'Affinity', max_length=20, choices=[(b'Affinity', b'affinity'), (b'Anti-Affinity', b'anti-affinity')])),
                ('reason', models.CharField(default=b'', max_length=256, null=True, blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='Component',
            fields=[
                ('commit_id', models.UUIDField(auto_created=True, primary_key=True, default=uuid.uuid4, serialize=False, editable=False)),
                ('latest', models.BooleanField(default=True, editable=False)),
                ('changed_from', models.UUIDField(default=None, null=True, editable=False, blank=True)),
                ('tag', models.CharField(default=b'', max_length=50, blank=True)),
                ('commit_time', models.DateTimeField(auto_now_add=True)),
                ('name', models.CharField(max_length=256, db_index=True)),
                ('description', models.CharField(default=b'', max_length=256, null=True, blank=True)),
                ('host_network', models.BooleanField(default=False)),
                ('mem_per_instance', models.FloatField(default=128)),
                ('cpu_per_instance', models.FloatField(default=0.125)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='ComponentRelease',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('quantity', models.IntegerField(default=1)),
                ('component', models.ForeignKey(related_name='deploy_comp', default=None, to='alchimest.Component')),
            ],
        ),
        migrations.CreateModel(
            name='Employee',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
            ],
        ),
        migrations.CreateModel(
            name='EnvironmentVariable',
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
            name='Image',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=256, db_index=True)),
                ('version', models.CharField(max_length=128)),
            ],
        ),
        migrations.CreateModel(
            name='Namespace',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=256, db_index=True)),
            ],
        ),
        migrations.CreateModel(
            name='Package',
            fields=[
                ('commit_id', models.UUIDField(auto_created=True, primary_key=True, default=uuid.uuid4, serialize=False, editable=False)),
                ('latest', models.BooleanField(default=True, editable=False)),
                ('changed_from', models.UUIDField(default=None, null=True, editable=False, blank=True)),
                ('tag', models.CharField(default=b'', max_length=50, blank=True)),
                ('commit_time', models.DateTimeField(auto_now_add=True)),
                ('name', models.CharField(max_length=128)),
                ('description', models.CharField(default=b'', max_length=256, null=True, blank=True)),
                ('components', models.ManyToManyField(default=None, to='alchimest.Component', through='alchimest.ComponentRelease')),
                ('namespace', models.ForeignKey(to='alchimest.Namespace')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Port',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(default=b'port-', max_length=128)),
                ('container_port', models.CharField(default=b'80', max_length=128)),
                ('protocol', models.CharField(default=b'TCP', max_length=20, choices=[(b'TCP', b'tcp'), (b'UDP', b'udp')])),
                ('component', models.ForeignKey(related_name='port_of_comp', default=None, to='alchimest.Component')),
            ],
        ),
        migrations.CreateModel(
            name='VolumeClaim',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('pvc_name', models.CharField(default=b'vol-', max_length=128)),
                ('container_path', models.CharField(default=b'/', max_length=128)),
                ('mode', models.CharField(default=b'Read&Write', max_length=20, choices=[(b'Read&Write', b'rw'), (b'ReadOnly', b'ro')])),
                ('type', models.CharField(default=b'EMPTY', max_length=20, choices=[(b'EMPTY', b'emptyDir'), (b'HOST', b'hostPath'), (b'SECRET', b'secret')])),
                ('component', models.ForeignKey(related_name='vol_of_comp', default=None, to='alchimest.Component')),
            ],
        ),
        migrations.AlterUniqueTogether(
            name='namespace',
            unique_together=set([('name',)]),
        ),
        migrations.AddField(
            model_name='image',
            name='namespace',
            field=models.ForeignKey(to='alchimest.Namespace'),
        ),
        migrations.AddField(
            model_name='employee',
            name='own_namespaces',
            field=models.ManyToManyField(to='alchimest.Namespace'),
        ),
        migrations.AddField(
            model_name='employee',
            name='user',
            field=models.OneToOneField(to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='componentrelease',
            name='in_package',
            field=models.ForeignKey(related_name='in_package', default=None, to='alchimest.Package'),
        ),
        migrations.AddField(
            model_name='component',
            name='image',
            field=models.ForeignKey(to='alchimest.Image'),
        ),
        migrations.AddField(
            model_name='component',
            name='namespace',
            field=models.ForeignKey(to='alchimest.Namespace'),
        ),
        migrations.AddField(
            model_name='affinity',
            name='from_component',
            field=models.ForeignKey(related_name='affinity_from_component', to='alchimest.Component'),
        ),
        migrations.AddField(
            model_name='affinity',
            name='to_component',
            field=models.ForeignKey(related_name='affinity_to_component', to='alchimest.Component'),
        ),
        migrations.AlterUniqueTogether(
            name='image',
            unique_together=set([('namespace', 'name', 'version')]),
        ),
    ]
