# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('alchimest', '0003_auto_20180428_1133'),
    ]

    operations = [
        migrations.RenameField(
            model_name='affinity',
            old_name='from_component',
            new_name='component',
        ),
    ]
