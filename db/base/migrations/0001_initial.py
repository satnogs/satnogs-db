# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.db.models.deletion
from django.conf import settings
import django.core.validators


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Satellite',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('norad_cat_id', models.PositiveIntegerField()),
                ('name', models.CharField(max_length=45)),
            ],
        ),
        migrations.CreateModel(
            name='Transponder',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('description', models.TextField()),
                ('alive', models.BooleanField(default=True)),
                ('uplink_low', models.PositiveIntegerField(null=True, blank=True)),
                ('uplink_high', models.PositiveIntegerField(null=True, blank=True)),
                ('downlink_low', models.PositiveIntegerField(null=True, blank=True)),
                ('downlink_high', models.PositiveIntegerField(null=True, blank=True)),
                ('mode', models.CharField(max_length=10, choices=[(b'FM', b'FM'), (b'AFSK', b'AFSK'), (b'BFSK', b'BFSK'), (b'APRS', b'APRS'), (b'SSTV', b'SSTV'), (b'CW', b'CW'), (b'FMN', b'FMN')])),
                ('invert', models.BooleanField(default=False)),
                ('baud', models.FloatField(validators=[django.core.validators.MinValueValidator(0)])),
                ('approved', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='Suggestion',
            fields=[
                ('transponder_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='base.Transponder')),
                ('citation', models.CharField(max_length=255, blank=True)),
            ],
            bases=('base.transponder',),
        ),
        migrations.AddField(
            model_name='transponder',
            name='satellite',
            field=models.ForeignKey(related_name='transponders', to='base.Satellite', null=True),
        ),
        migrations.AddField(
            model_name='suggestion',
            name='transponder',
            field=models.ForeignKey(related_name='suggestions', on_delete=django.db.models.deletion.SET_NULL, blank=True, to='base.Transponder', null=True),
        ),
        migrations.AddField(
            model_name='suggestion',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.SET_NULL, blank=True, to=settings.AUTH_USER_MODEL, null=True),
        ),
    ]
