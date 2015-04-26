# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0003_auto_20150425_1844'),
    ]

    operations = [
        migrations.AddField(
            model_name='transponder',
            name='approved',
            field=models.BooleanField(default=False),
        ),
    ]
