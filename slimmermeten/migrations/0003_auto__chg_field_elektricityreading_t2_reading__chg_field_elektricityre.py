# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):

        # Changing field 'ElektricityReading.t2_reading'
        db.alter_column(u'slimmermeten_elektricityreading', 't2_reading', self.gf('django.db.models.fields.DecimalField')(max_digits=12, decimal_places=2))

        # Changing field 'ElektricityReading.t1_reading'
        db.alter_column(u'slimmermeten_elektricityreading', 't1_reading', self.gf('django.db.models.fields.DecimalField')(max_digits=12, decimal_places=2))

        # Changing field 'ElektricityReading.t1_back_reading'
        db.alter_column(u'slimmermeten_elektricityreading', 't1_back_reading', self.gf('django.db.models.fields.DecimalField')(max_digits=12, decimal_places=2))

        # Changing field 'ElektricityReading.t2_back_reading'
        db.alter_column(u'slimmermeten_elektricityreading', 't2_back_reading', self.gf('django.db.models.fields.DecimalField')(max_digits=12, decimal_places=2))

    def backwards(self, orm):

        # Changing field 'ElektricityReading.t2_reading'
        db.alter_column(u'slimmermeten_elektricityreading', 't2_reading', self.gf('django.db.models.fields.IntegerField')())

        # Changing field 'ElektricityReading.t1_reading'
        db.alter_column(u'slimmermeten_elektricityreading', 't1_reading', self.gf('django.db.models.fields.IntegerField')())

        # Changing field 'ElektricityReading.t1_back_reading'
        db.alter_column(u'slimmermeten_elektricityreading', 't1_back_reading', self.gf('django.db.models.fields.IntegerField')())

        # Changing field 'ElektricityReading.t2_back_reading'
        db.alter_column(u'slimmermeten_elektricityreading', 't2_back_reading', self.gf('django.db.models.fields.IntegerField')())

    models = {
        'slimmermeten.elektricityreading': {
            'Meta': {'object_name': 'ElektricityReading'},
            'date': ('django.db.models.fields.DateTimeField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            't1_back_reading': ('django.db.models.fields.DecimalField', [], {'default': '0', 'max_digits': '12', 'decimal_places': '2'}),
            't1_reading': ('django.db.models.fields.DecimalField', [], {'default': '0', 'max_digits': '12', 'decimal_places': '2'}),
            't2_back_reading': ('django.db.models.fields.DecimalField', [], {'default': '0', 'max_digits': '12', 'decimal_places': '2'}),
            't2_reading': ('django.db.models.fields.DecimalField', [], {'default': '0', 'max_digits': '12', 'decimal_places': '2'}),
            'tarief': ('django.db.models.fields.IntegerField', [], {'default': '0'})
        },
        'slimmermeten.gasreading': {
            'Meta': {'object_name': 'GasReading'},
            'date': ('django.db.models.fields.DateTimeField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'reading': ('django.db.models.fields.IntegerField', [], {'default': '0'})
        },
        'slimmermeten.powerconsumption': {
            'Meta': {'object_name': 'PowerConsumption'},
            'date': ('django.db.models.fields.DateTimeField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'power': ('django.db.models.fields.IntegerField', [], {'default': '0'})
        }
    }

    complete_apps = ['slimmermeten']