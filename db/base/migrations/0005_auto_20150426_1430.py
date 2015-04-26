# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0004_transponder_approved'),
    ]

    operations = [
        migrations.AlterField(
            model_name='suggestion',
            name='citation',
            field=models.CharField(max_length=255, blank=True),
        ),
    ]
