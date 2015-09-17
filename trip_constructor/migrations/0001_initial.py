# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'UserProfile'
        db.create_table(u'visa8_userprofile', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'], unique=True)),
            ('picture', self.gf('django.db.models.fields.files.ImageField')(max_length=100, blank=True)),
            ('country', self.gf('django_countries.fields.CountryField')(max_length=2, blank=True)),
        ))
        db.send_create_signal(u'visa8', ['UserProfile'])

        # Adding model 'Requirements'
        db.create_table(u'visa8_requirements', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('flag', self.gf('django.db.models.fields.files.ImageField')(max_length=100)),
            ('nationality', self.gf('django_countries.fields.CountryField')(max_length=2)),
            ('destination', self.gf('django_countries.fields.CountryField')(max_length=2)),
            ('visa_required', self.gf('django.db.models.fields.CharField')(max_length=20)),
            ('notes', self.gf('django.db.models.fields.CharField')(max_length=1000)),
        ))
        db.send_create_signal(u'visa8', ['Requirements'])

        # Adding model 'Trip'
        db.create_table(u'visa8_trip', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'])),
            ('your_requirements', self.gf('django.db.models.fields.related.ForeignKey')(related_name='your_requirements_for_trip', to=orm['visa8.Requirements'])),
            ('partner_requirements', self.gf('django.db.models.fields.related.ForeignKey')(related_name='partner_requirements_for_trip', to=orm['visa8.Requirements'])),
        ))
        db.send_create_signal(u'visa8', ['Trip'])


    def backwards(self, orm):
        # Deleting model 'UserProfile'
        db.delete_table(u'visa8_userprofile')

        # Deleting model 'Requirements'
        db.delete_table(u'visa8_requirements')

        # Deleting model 'Trip'
        db.delete_table(u'visa8_trip')


    models = {
        u'auth.group': {
            'Meta': {'object_name': 'Group'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        u'auth.permission': {
            'Meta': {'ordering': "(u'content_type__app_label', u'content_type__model', u'codename')", 'unique_together': "((u'content_type', u'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['contenttypes.ContentType']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        u'auth.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "u'user_set'", 'blank': 'True', 'to': u"orm['auth.Group']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "u'user_set'", 'blank': 'True', 'to': u"orm['auth.Permission']"}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        u'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        u'visa8.requirements': {
            'Meta': {'object_name': 'Requirements'},
            'destination': ('django_countries.fields.CountryField', [], {'max_length': '2'}),
            'flag': ('django.db.models.fields.files.ImageField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'nationality': ('django_countries.fields.CountryField', [], {'max_length': '2'}),
            'notes': ('django.db.models.fields.CharField', [], {'max_length': '1000'}),
            'visa_required': ('django.db.models.fields.CharField', [], {'max_length': '20'})
        },
        u'visa8.trip': {
            'Meta': {'object_name': 'Trip'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'partner_requirements': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'partner_requirements_for_trip'", 'to': u"orm['visa8.Requirements']"}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.User']"}),
            'your_requirements': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'your_requirements_for_trip'", 'to': u"orm['visa8.Requirements']"})
        },
        u'visa8.userprofile': {
            'Meta': {'object_name': 'UserProfile'},
            'country': ('django_countries.fields.CountryField', [], {'max_length': '2', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'picture': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'blank': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.User']", 'unique': 'True'})
        }
    }

    complete_apps = ['visa8']