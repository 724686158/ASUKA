# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('alchimest', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='component',
            name='commit_time',
        ),
        migrations.RemoveField(
            model_name='package',
            name='commit_time',
        ),
    ]
