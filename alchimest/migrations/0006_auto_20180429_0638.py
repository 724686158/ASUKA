# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('alchimest', '0005_auto_20180429_0626'),
    ]

    operations = [
        migrations.AddField(
            model_name='component',
            name='commit_time',
            field=models.DateTimeField(default=datetime.datetime(2018, 4, 29, 6, 38, 29, 613411, tzinfo=utc), auto_now_add=True),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='package',
            name='commit_time',
            field=models.DateTimeField(default=datetime.datetime(2018, 4, 29, 6, 38, 34, 431628, tzinfo=utc), auto_now_add=True),
            preserve_default=False,
        ),
    ]
