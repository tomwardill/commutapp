# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding model 'Incident'
        db.create_table('main_incident', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('description', self.gf('django.db.models.fields.TextField')()),
            ('location', self.gf('django.contrib.gis.db.models.fields.PointField')()),
        ))
        db.send_create_signal('main', ['Incident'])

        # Adding model 'CurrentRoad'
        db.create_table('main_currentroad', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('update_time', self.gf('django.db.models.fields.DateTimeField')()),
        ))
        db.send_create_signal('main', ['CurrentRoad'])


    def backwards(self, orm):
        
        # Deleting model 'Incident'
        db.delete_table('main_incident')

        # Deleting model 'CurrentRoad'
        db.delete_table('main_currentroad')


    models = {
        'main.currentroad': {
            'Meta': {'object_name': 'CurrentRoad'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'update_time': ('django.db.models.fields.DateTimeField', [], {})
        },
        'main.incident': {
            'Meta': {'object_name': 'Incident'},
            'description': ('django.db.models.fields.TextField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'location': ('django.contrib.gis.db.models.fields.PointField', [], {})
        }
    }

    complete_apps = ['main']
