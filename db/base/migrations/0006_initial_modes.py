# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.core.management import call_command


def add_modes(apps, schema_editor):
    call_command('loaddata', 'modes', app_label='base')

class Migration(migrations.Migration):

    dependencies = [
        ('base', '0005_auto_20150813_1112'),
    ]

    operations = [
        migrations.RunPython(add_modes),
    ]
