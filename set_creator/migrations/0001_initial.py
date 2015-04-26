# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('practice', '0004_extendedcontext_fullname'),
    ]

    operations = [
        migrations.CreateModel(
            name='Set',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=255)),
                ('active', models.BooleanField(default=True)),
                ('terms', models.ManyToManyField(to='practice.ExtendedTerm')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
