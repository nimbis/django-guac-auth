# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models, connection
import guac_auth.fields


class Migration(migrations.Migration):

    def enums_forward(apps, schema_editor):
        # SQLite (tests) does not have ENUMs, so don't run then during tests.
        # Required for Postgres however.
        if schema_editor.connection.vendor == 'sqlite':
            return
        cursor = connection.cursor()

        cursor.execute("CREATE TYPE guacamole_connection_group_type AS ENUM( 'ORGANIZATIONAL', 'BALANCING');")
        cursor.execute("CREATE TYPE guacamole_object_permission_type AS ENUM( 'READ', 'UPDATE', 'DELETE', 'ADMINISTER');")
        cursor.execute("CREATE TYPE guacamole_system_permission_type AS ENUM( 'CREATE_CONNECTION', 'CREATE_CONNECTION_GROUP', 'CREATE_USER', 'ADMINISTER');")

    def enums_reverse(apps, schema_editor):
        # SQLite (tests) does not have ENUMs, so don't run then during tests.
        # Required for Postgres however.
        if schema_editor.connection.vendor == 'sqlite':
            return
        cursor = connection.cursor()

        cursor.execute("DROP TYPE guacamole_connection_group_type")
        cursor.execute("DROP TYPE guacamole_object_permission_type")
        cursor.execute("DROP TYPE guacamole_system_permission_type")

    dependencies = [
        ('guac_auth', '0002_auto_20160128_1752'),
    ]

    operations = [
        migrations.RunPython(enums_forward, enums_reverse),
        migrations.AddField(
            model_name='guacamoleconnectiongroup',
            name='type',
            field=guac_auth.fields.GuacamoleConnectionGroupTypeField(default=b'ORGANIZATIONAL', choices=[(b'ORGANIZATIONAL', b'ORGANIZATIONAL'), (b'BALANCING', b'BALANCING')]),
        ),
        migrations.AddField(
            model_name='guacamoleconnectiongrouppermission',
            name='permission',
            field=guac_auth.fields.GuacamoleObjectPermissionTypeField(default=b'READ', choices=[(b'READ', b'READ'), (b'UPDATE', b'UPDATE'), (b'DELETE', b'DELETE'), (b'ADMINISTER', b'ADMINISTER')]),
        ),
        migrations.AddField(
            model_name='guacamoleconnectionpermission',
            name='permission',
            field=guac_auth.fields.GuacamoleObjectPermissionTypeField(default=b'READ', choices=[(b'READ', b'READ'), (b'UPDATE', b'UPDATE'), (b'DELETE', b'DELETE'), (b'ADMINISTER', b'ADMINISTER')]),
        ),
        migrations.AddField(
            model_name='guacamolesystempermission',
            name='permission',
            field=guac_auth.fields.GuacamoleSystemPermissionTypeField(default=b'CREATE_CONNECTION', choices=[(b'CREATE_CONNECTION', b'CREATE_CONNECTION'), (b'CREATE_CONNECTION_GROUP', b'CREATE_CONNECTION_GROUP'), (b'CREATE_USER', b'CREATE_USER'), (b'ADMINISTER', b'ADMINISTER')]),
        ),
        migrations.AddField(
            model_name='guacamoleuserpermission',
            name='permission',
            field=guac_auth.fields.GuacamoleObjectPermissionTypeField(default=b'READ', choices=[(b'READ', b'READ'), (b'UPDATE', b'UPDATE'), (b'DELETE', b'DELETE'), (b'ADMINISTER', b'ADMINISTER')]),
        ),
        migrations.AlterUniqueTogether(
            name='guacamoleconnectiongrouppermission',
            unique_together=set([('user', 'connection_group', 'permission')]),
        ),
        migrations.AlterUniqueTogether(
            name='guacamoleconnectionpermission',
            unique_together=set([('user', 'connection', 'permission')]),
        ),
        migrations.AlterUniqueTogether(
            name='guacamolesystempermission',
            unique_together=set([('user', 'permission')]),
        ),
        migrations.AlterUniqueTogether(
            name='guacamoleuserpermission',
            unique_together=set([('user', 'affected_user', 'permission')]),
        ),
    ]
