# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.db.models.deletion
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('base', '0002_auto_20150425_1633'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Suggestion',
        ),
        migrations.RemoveField(
            model_name='transponder',
            name='approved',
        ),
        migrations.RemoveField(
            model_name='transponder',
            name='citation',
        ),
        migrations.RemoveField(
            model_name='transponder',
            name='suggestion',
        ),
        migrations.RemoveField(
            model_name='transponder',
            name='user',
        ),
        migrations.CreateModel(
            name='Suggestion',
            fields=[
                ('transponder_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='base.Transponder')),
                ('citation', models.URLField(max_length=255, blank=True)),
                ('transponder', models.ForeignKey(related_name='suggestions', on_delete=django.db.models.deletion.SET_NULL, blank=True, to='base.Transponder', null=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.SET_NULL, blank=True, to=settings.AUTH_USER_MODEL, null=True)),
            ],
            bases=('base.transponder',),
        ),
    ]
