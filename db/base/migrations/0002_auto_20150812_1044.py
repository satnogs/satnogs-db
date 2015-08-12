# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='satellite',
            options={'ordering': ['name']},
        ),
        migrations.AddField(
            model_name='satellite',
            name='image',
            field=models.ImageField(upload_to=b'satellites', blank=True),
        ),
        migrations.AddField(
            model_name='satellite',
            name='names',
            field=models.TextField(blank=True),
        ),
    ]
