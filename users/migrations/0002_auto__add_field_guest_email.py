# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'Guest.email'
        db.add_column(u'users_guest', 'email',
                      self.gf('django.db.models.fields.EmailField')(default='default@firestopapp.com', max_length=75),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting field 'Guest.email'
        db.delete_column(u'users_guest', 'email')


    models = {
        u'users.guest': {
            'Meta': {'object_name': 'Guest'},
            'department': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'position': ('django.db.models.fields.CharField', [], {'max_length': '63'})
        }
    }

    complete_apps = ['users']