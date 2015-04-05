# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('practice', '0002_auto_20150404_1552'),
    ]

    operations = [
        migrations.AddField(
            model_name='extendedterm',
            name='interesting',
            field=models.TextField(null=True, blank=True),
            preserve_default=True,
        ),
    ]
