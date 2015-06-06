# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('practice', '0005_auto_20150428_0444'),
    ]

    operations = [
        migrations.CreateModel(
            name='Request',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('original_id', models.IntegerField(unique=True)),
                ('images', models.TextField()),
                ('lat', models.FloatField(null=True, blank=True)),
                ('long', models.FloatField(null=True, blank=True)),
                ('created', models.DateTimeField(auto_now=True)),
                ('term', models.ForeignKey(to='practice.ExtendedTerm', null=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
