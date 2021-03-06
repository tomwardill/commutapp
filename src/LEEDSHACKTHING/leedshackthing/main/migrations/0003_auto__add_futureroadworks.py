# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding model 'FutureRoadWorks'
        db.create_table('main_futureroadworks', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('description', self.gf('django.db.models.fields.TextField')()),
            ('location', self.gf('django.contrib.gis.db.models.fields.PointField')()),
            ('start_time', self.gf('django.db.models.fields.DateTimeField')()),
            ('end_time', self.gf('django.db.models.fields.DateTimeField')()),
        ))
        db.send_create_signal('main', ['FutureRoadWorks'])


    def backwards(self, orm):
        
        # Deleting model 'FutureRoadWorks'
        db.delete_table('main_futureroadworks')


    models = {
        'main.currentroadworks': {
            'Meta': {'object_name': 'CurrentRoadWorks'},
            'description': ('django.db.models.fields.TextField', [], {}),
            'end_time': ('django.db.models.fields.DateTimeField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'location': ('django.contrib.gis.db.models.fields.PointField', [], {}),
            'start_time': ('django.db.models.fields.DateTimeField', [], {})
        },
        'main.futureroadworks': {
            'Meta': {'object_name': 'FutureRoadWorks'},
            'description': ('django.db.models.fields.TextField', [], {}),
            'end_time': ('django.db.models.fields.DateTimeField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'location': ('django.contrib.gis.db.models.fields.PointField', [], {}),
            'start_time': ('django.db.models.fields.DateTimeField', [], {})
        },
        'main.incident': {
            'Meta': {'object_name': 'Incident'},
            'description': ('django.db.models.fields.TextField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'location': ('django.contrib.gis.db.models.fields.PointField', [], {})
        }
    }

    complete_apps = ['main']
