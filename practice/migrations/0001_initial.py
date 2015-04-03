# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('proso_flashcards', '0005_auto_20150330_0513'),
    ]

    operations = [
        migrations.CreateModel(
            name='ExtendedContext',
            fields=[
                ('context_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='proso_flashcards.Context')),
            ],
            options={
            },
            bases=('proso_flashcards.context',),
        ),
        migrations.CreateModel(
            name='ExtendedTerm',
            fields=[
                ('term_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='proso_flashcards.Term')),
                ('url', models.TextField()),
            ],
            options={
            },
            bases=('proso_flashcards.term',),
        ),
    ]
