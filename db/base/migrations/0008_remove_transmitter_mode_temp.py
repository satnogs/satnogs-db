# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0007_mv_modes'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='transmitter',
            name='mode_temp',
        ),
    ]
