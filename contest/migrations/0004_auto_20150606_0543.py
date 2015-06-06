# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('contest', '0003_auto_20150606_0437'),
    ]

    operations = [
        migrations.AlterField(
            model_name='guess',
            name='correct',
            field=models.CharField(blank=True, max_length=2, null=True, choices=[(b'c', b'correct'), (b'i', b'incorrect'), (b'pc', b'partially correct')]),
            preserve_default=True,
        ),
    ]
