# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('practice', '0005_auto_20150428_0444'),
        ('contest', '0002_auto_20150606_0327'),
    ]

    operations = [
        migrations.CreateModel(
            name='Guess',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('correct', models.NullBooleanField()),
                ('points', models.IntegerField(null=True, blank=True)),
                ('delay', models.IntegerField(null=True, blank=True)),
                ('request', models.ForeignKey(related_name='guesses', to='contest.Request')),
                ('term', models.ForeignKey(to='practice.ExtendedTerm')),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='request',
            name='closed',
            field=models.BooleanField(default=False),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='request',
            name='created',
            field=models.DateTimeField(auto_now_add=True),
            preserve_default=True,
        ),
    ]
