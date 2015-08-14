# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


def mv_modes(apps, schema_editor):
    Transmitter = apps.get_model('base', 'Transmitter')
    Mode = apps.get_model('base', 'Mode')
    for transmitter in Transmitter.objects.all():
        try:
            mode = Mode.objects.get(name=transmitter.mode_temp)
            transmitter.mode = mode
        except Mode.DoesNotExist:
            transmitter.mode = None
        transmitter.save()

class Migration(migrations.Migration):

    dependencies = [
        ('base', '0007_initial_modes'),
    ]

    operations = [
        migrations.RunPython(mv_modes),
    ]
