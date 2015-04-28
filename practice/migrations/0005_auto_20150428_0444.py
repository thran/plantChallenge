# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('proso_flashcards', '0006_auto_20150414_0946'),
        ('practice', '0004_extendedcontext_fullname'),
    ]

    operations = [
        migrations.CreateModel(
            name='Request',
            fields=[
            ],
            options={
                'proxy': True,
            },
            bases=('proso_flashcards.flashcard',),
        ),
        migrations.AlterModelOptions(
            name='extendedcontext',
            options={'verbose_name': 'Request'},
        ),
        migrations.AlterModelOptions(
            name='extendedterm',
            options={'verbose_name': 'Plant'},
        ),
    ]
