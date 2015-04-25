# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('practice', '0003_extendedterm_interesting'),
    ]

    operations = [
        migrations.AddField(
            model_name='extendedcontext',
            name='fullname',
            field=models.CharField(max_length=255, null=True, blank=True),
            preserve_default=True,
        ),
    ]
