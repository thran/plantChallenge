# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
#
# Also note: You'll have to insert the output of 'django-admin.py sqlcustom [app_label]'
# into your database.
from __future__ import unicode_literals

from django.db import models


class Answer(models.Model):
    request = models.ForeignKey('Request', db_column="request_id", primary_key=True)
    url = models.TextField(blank=True)
    answer = models.TextField(blank=True)
    note = models.TextField(blank=True)
    author = models.CharField(max_length=15, blank=True)
    twid = models.CharField(max_length=30, blank=True)
    hash = models.CharField(max_length=50, blank=True)
    sureness = models.IntegerField()
    user_response = models.CharField(max_length=10, blank=True)
    timestamp = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'answer'


class Flowers(models.Model):
    id = models.IntegerField(primary_key=True)  # AutoField?
    name = models.TextField()
    wikilink = models.TextField()
    counter = models.IntegerField()
    lang = models.CharField(max_length=3, blank=True)
    botanist = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'flowers'


class Imagefile(models.Model):
    request = models.ForeignKey('Request', db_column='request')
    imgorder = models.IntegerField()
    type = models.CharField(max_length=9)
    filename = models.CharField(max_length=100)
    addedas = models.CharField(max_length=20, blank=True)
    accesshash = models.CharField(max_length=20, blank=True)
    clouded = models.CharField(max_length=3)
    timestamp = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'imagefile'


class ImportedPlants(models.Model):
    fullname = models.CharField(primary_key=True, max_length=300)
    genus = models.CharField(max_length=300)
    url = models.CharField(max_length=1000)
    commonnames = models.CharField(max_length=1000)
    synonyms = models.CharField(max_length=1000)
    epiphyte = models.CharField(max_length=300)
    note = models.CharField(max_length=1000)
    database = models.CharField(max_length=5)

    class Meta:
        managed = False
        db_table = 'imported-plants'


class PlantType(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=25)

    class Meta:
        managed = False
        db_table = 'plant_type'


class Request(models.Model):
    id = models.IntegerField(primary_key=True)  # AutoField?
    user_id = models.IntegerField(blank=True, null=True)
    updated = models.DateTimeField(blank=True, null=True)
    status = models.CharField(max_length=10)
    question = models.CharField(max_length=900, blank=True)
    gps = models.CharField(max_length=60, blank=True)
    created = models.DateTimeField()
    twid = models.BigIntegerField(blank=True, null=True)
    valid = models.TextField(blank=True)
    user_description = models.TextField(blank=True)
    source = models.CharField(max_length=7, blank=True)
    access_hash = models.CharField(max_length=12, blank=True)
    country = models.CharField(max_length=5, blank=True)
    unresolvedreason = models.TextField(blank=True)
    plant_type = models.IntegerField(blank=True, null=True)
    ip = models.CharField(max_length=40, blank=True)
    alchemyapi = models.CharField(max_length=50, blank=True)
    deviceid = models.CharField(max_length=300, blank=True)
    platform = models.CharField(max_length=10, blank=True)
    imgproblem = models.IntegerField(blank=True, null=True)
    herbarium_status = models.CharField(max_length=7)
    elevation = models.IntegerField(blank=True, null=True)
    mobile_status = models.CharField(max_length=30, blank=True)
    zipcode = models.CharField(max_length=20, blank=True)

    class Meta:
        managed = False
        db_table = 'request'
