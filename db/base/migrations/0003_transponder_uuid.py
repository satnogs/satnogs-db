# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import shortuuidfield.fields


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0002_auto_20150509_0806'),
    ]

    operations = [
        migrations.AddField(
            model_name='transponder',
            name='uuid',
            field=shortuuidfield.fields.ShortUUIDField(db_index=True, unique=True, max_length=22, editable=False, blank=True),
        ),
    ]
