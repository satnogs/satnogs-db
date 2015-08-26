# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings
import django.db.models.deletion
import shortuuidfield.fields
import django.core.validators


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Mode',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(unique=True, max_length=10)),
            ],
        ),
        migrations.CreateModel(
            name='Satellite',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('norad_cat_id', models.PositiveIntegerField()),
                ('name', models.CharField(max_length=45)),
                ('names', models.TextField(blank=True)),
                ('image', models.ImageField(upload_to=b'satellites', blank=True)),
            ],
            options={
                'ordering': ['name'],
            },
        ),
        migrations.CreateModel(
            name='Transmitter',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('uuid', shortuuidfield.fields.ShortUUIDField(db_index=True, unique=True, max_length=22, editable=False, blank=True)),
                ('description', models.TextField()),
                ('alive', models.BooleanField(default=True)),
                ('uplink_low', models.PositiveIntegerField(null=True, blank=True)),
                ('uplink_high', models.PositiveIntegerField(null=True, blank=True)),
                ('downlink_low', models.PositiveIntegerField(null=True, blank=True)),
                ('downlink_high', models.PositiveIntegerField(null=True, blank=True)),
                ('invert', models.BooleanField(default=False)),
                ('baud', models.FloatField(blank=True, null=True, validators=[django.core.validators.MinValueValidator(0)])),
                ('approved', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='Suggestion',
            fields=[
                ('transmitter_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='base.Transmitter')),
                ('citation', models.CharField(max_length=255, blank=True)),
            ],
            bases=('base.transmitter',),
        ),
        migrations.AddField(
            model_name='transmitter',
            name='mode',
            field=models.ForeignKey(related_name='transmitters', on_delete=django.db.models.deletion.SET_NULL, blank=True, to='base.Mode', null=True),
        ),
        migrations.AddField(
            model_name='transmitter',
            name='satellite',
            field=models.ForeignKey(related_name='transmitters', to='base.Satellite', null=True),
        ),
        migrations.AddField(
            model_name='suggestion',
            name='transmitter',
            field=models.ForeignKey(related_name='suggestions', on_delete=django.db.models.deletion.SET_NULL, blank=True, to='base.Transmitter', null=True),
        ),
        migrations.AddField(
            model_name='suggestion',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.SET_NULL, blank=True, to=settings.AUTH_USER_MODEL, null=True),
        ),
    ]
