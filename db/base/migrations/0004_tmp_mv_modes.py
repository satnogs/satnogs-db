# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


def tmp_mv_modes(apps, schema_editor):
    Transmitter = apps.get_model('base', 'Transmitter')
    for transmitter in Transmitter.objects.all():
        transmitter.mode_temp = transmitter.mode
        transmitter.save()


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0003_auto_20150813_1108'),
    ]

    operations = [
        migrations.RunPython(tmp_mv_modes),
    ]
