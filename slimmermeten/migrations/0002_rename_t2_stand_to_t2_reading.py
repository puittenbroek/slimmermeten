# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        db.rename_column('slimmermeten_elektricityreading', 't2_stand', 't2_reading')

    def backwards(self, orm):
        db.rename_column('slimmermeten_elektricityreading', 't2_reading', 't2_stand')

    models = {
        u'slimmermeten.elektricityreading': {
            'Meta': {'object_name': 'ElektricityReading'},
            'date': ('django.db.models.fields.DateTimeField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            't1_back_reading': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            't1_reading': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            't2_back_reading': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            't2_reading': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'tarief': ('django.db.models.fields.IntegerField', [], {'default': '0'})
        },
        u'slimmermeten.gasreading': {
            'Meta': {'object_name': 'GasReading'},
            'date': ('django.db.models.fields.DateTimeField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'reading': ('django.db.models.fields.IntegerField', [], {'default': '0'})
        },
        u'slimmermeten.powerconsumption': {
            'Meta': {'object_name': 'PowerConsumption'},
            'date': ('django.db.models.fields.DateTimeField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'power': ('django.db.models.fields.IntegerField', [], {'default': '0'})
        }
    }

    complete_apps = ['slimmermeten']