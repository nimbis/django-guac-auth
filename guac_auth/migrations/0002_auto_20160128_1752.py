# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('guac_auth', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='guacamoleconnectiongroup',
            name='type',
        ),
        migrations.AlterUniqueTogether(
            name='guacamoleconnectiongrouppermission',
            unique_together=set([]),
        ),
        migrations.AlterUniqueTogether(
            name='guacamoleconnectionpermission',
            unique_together=set([]),
        ),
        migrations.AlterUniqueTogether(
            name='guacamolesystempermission',
            unique_together=set([]),
        ),
        migrations.AlterUniqueTogether(
            name='guacamoleuserpermission',
            unique_together=set([]),
        ),
        migrations.RemoveField(
            model_name='guacamoleconnectiongrouppermission',
            name='permission',
        ),
        migrations.RemoveField(
            model_name='guacamoleconnectionpermission',
            name='permission',
        ),
        migrations.RemoveField(
            model_name='guacamolesystempermission',
            name='permission',
        ),
        migrations.RemoveField(
            model_name='guacamoleuserpermission',
            name='permission',
        ),
    ]
