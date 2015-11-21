# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('proso_flashcards', '0011_remove_flashcardanswer_meta'),
        ('practice', '0005_auto_20150428_0444'),
    ]

    operations = [
        migrations.AddField(
            model_name='extendedterm',
            name='example',
            field=models.ForeignKey(blank=True, to='proso_flashcards.Flashcard', null=True),
            preserve_default=True,
        ),
    ]
