# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='satellite',
            name='image',
            field=models.ImageField(help_text=b'Ideally: 250x250', upload_to=b'satellites', blank=True),
        ),
    ]
