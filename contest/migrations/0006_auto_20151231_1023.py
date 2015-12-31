# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('contest', '0005_auto_20151213_0441'),
    ]

    operations = [
        migrations.CreateModel(
            name='Location',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('lat', models.FloatField(null=True, blank=True)),
                ('long', models.FloatField(null=True, blank=True)),
                ('country', models.CharField(max_length=50, null=True, blank=True)),
                ('source', models.TextField(null=True, blank=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='request',
            name='location',
            field=models.ForeignKey(blank=True, to='contest.Location', null=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='guess',
            name='correct',
            field=models.CharField(blank=True, max_length=2, null=True, choices=[(b'c', b'correct'), (b'i', b'incorrect'), (b'pc', b'partially correct'), (b'wd', b"we don't know")]),
            preserve_default=True,
        ),
    ]
