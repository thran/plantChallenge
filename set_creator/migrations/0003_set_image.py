# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('set_creator', '0002_set_for_daniel'),
    ]

    operations = [
        migrations.AddField(
            model_name='set',
            name='image',
            field=models.ImageField(null=True, upload_to=b'sets', blank=True),
            preserve_default=True,
        ),
    ]
