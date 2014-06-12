# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'ElektricityReading'
        db.create_table(u'slimmermeten_elektricityreading', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('date', self.gf('django.db.models.fields.DateTimeField')()),
            ('t1_reading', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('t1_back_reading', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('t2_stand', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('t2_back_reading', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('tarief', self.gf('django.db.models.fields.IntegerField')(default=0)),
        ))
        db.send_create_signal(u'slimmermeten', ['ElektricityReading'])

        # Adding model 'GasReading'
        db.create_table(u'slimmermeten_gasreading', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('date', self.gf('django.db.models.fields.DateTimeField')()),
            ('reading', self.gf('django.db.models.fields.IntegerField')(default=0)),
        ))
        db.send_create_signal(u'slimmermeten', ['GasReading'])

        # Adding model 'PowerConsumption'
        db.create_table(u'slimmermeten_powerconsumption', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('date', self.gf('django.db.models.fields.DateTimeField')()),
            ('power', self.gf('django.db.models.fields.IntegerField')(default=0)),
        ))
        db.send_create_signal(u'slimmermeten', ['PowerConsumption'])


    def backwards(self, orm):
        # Deleting model 'ElektricityReading'
        db.delete_table(u'slimmermeten_elektricityreading')

        # Deleting model 'GasReading'
        db.delete_table(u'slimmermeten_gasreading')

        # Deleting model 'PowerConsumption'
        db.delete_table(u'slimmermeten_powerconsumption')


    models = {
        u'slimmermeten.elektricityreading': {
            'Meta': {'object_name': 'ElektricityReading'},
            'date': ('django.db.models.fields.DateTimeField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            't1_back_reading': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            't1_reading': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            't2_back_reading': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            't2_stand': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
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