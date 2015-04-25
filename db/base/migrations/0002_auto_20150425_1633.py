# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.db.models.deletion
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('base', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Suggestion',
            fields=[
            ],
            options={
                'proxy': True,
            },
            bases=('base.transponder',),
        ),
        migrations.AddField(
            model_name='transponder',
            name='citation',
            field=models.URLField(max_length=255, blank=True),
        ),
        migrations.AddField(
            model_name='transponder',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.SET_NULL, blank=True, to=settings.AUTH_USER_MODEL, null=True),
        ),
        migrations.AlterField(
            model_name='transponder',
            name='satellite',
            field=models.ForeignKey(related_name='transponders', to='base.Satellite', null=True),
        ),
    ]
