# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('contest', '0004_auto_20150606_0543'),
    ]

    operations = [
        migrations.AlterField(
            model_name='guess',
            name='user',
            field=models.ForeignKey(related_name='guesses', to=settings.AUTH_USER_MODEL),
            preserve_default=True,
        ),
    ]
