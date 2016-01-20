# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='GuacamoleConnection',
            fields=[
                ('connection_id', models.AutoField(serialize=False, primary_key=True)),
                ('connection_name', models.CharField(max_length=128)),
                ('protocol', models.CharField(max_length=32)),
                ('max_connections', models.IntegerField(null=True, blank=True)),
                ('max_connections_per_user', models.IntegerField(null=True, blank=True)),
            ],
            options={
                'db_table': 'guacamole_connection',
            },
        ),
        migrations.CreateModel(
            name='GuacamoleConnectionGroup',
            fields=[
                ('connection_group_id', models.AutoField(serialize=False, primary_key=True)),
                ('connection_group_name', models.CharField(max_length=128)),
                ('type', models.CharField(default=b'ORGANIZATIONAL', max_length=128, choices=[(b'ORGANIZATIONAL', b'ORGANIZATIONAL'), (b'BALANCING', b'BALANCING')])),
                ('max_connections', models.IntegerField(null=True, blank=True)),
                ('max_connections_per_user', models.IntegerField(null=True, blank=True)),
                ('owner', models.ForeignKey(to=settings.AUTH_USER_MODEL, null=True)),
                ('parent', models.ForeignKey(related_name='child_groups', blank=True, to='guac_auth.GuacamoleConnectionGroup', null=True)),
            ],
            options={
                'db_table': 'guacamole_connection_group',
            },
        ),
        migrations.CreateModel(
            name='GuacamoleConnectionGroupPermission',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('permission', models.CharField(default=b'READ', max_length=128, choices=[(b'READ', b'READ'), (b'UPDATE', b'UPDATE'), (b'DELETE', b'DELETE'), (b'ADMINISTER', b'ADMINISTER')])),
                ('connection_group', models.ForeignKey(to='guac_auth.GuacamoleConnectionGroup')),
            ],
            options={
                'db_table': 'guacamole_connection_group_permission',
            },
        ),
        migrations.CreateModel(
            name='GuacamoleConnectionHistory',
            fields=[
                ('history_id', models.AutoField(serialize=False, primary_key=True)),
                ('start_date', models.DateTimeField()),
                ('end_date', models.DateTimeField(null=True, blank=True)),
                ('connection', models.ForeignKey(related_name='history', to='guac_auth.GuacamoleConnection')),
            ],
            options={
                'db_table': 'guacamole_connection_history',
            },
        ),
        migrations.CreateModel(
            name='GuacamoleConnectionParameter',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('parameter_name', models.CharField(max_length=128)),
                ('parameter_value', models.CharField(max_length=4096)),
                ('connection', models.ForeignKey(related_name='parameters', to='guac_auth.GuacamoleConnection')),
            ],
            options={
                'db_table': 'guacamole_connection_parameter',
            },
        ),
        migrations.CreateModel(
            name='GuacamoleConnectionPermission',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('permission', models.CharField(default=b'READ', max_length=128, choices=[(b'READ', b'READ'), (b'UPDATE', b'UPDATE'), (b'DELETE', b'DELETE'), (b'ADMINISTER', b'ADMINISTER')])),
                ('connection', models.ForeignKey(related_name='connection_permissions', to='guac_auth.GuacamoleConnection')),
            ],
            options={
                'db_table': 'guacamole_connection_permission',
            },
        ),
        migrations.CreateModel(
            name='GuacamoleSystemPermission',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('permission', models.CharField(max_length=128, choices=[(b'CREATE_CONNECTION', b'CREATE_CONNECTION'), (b'CREATE_CONNECTION_GROUP', b'CREATE_CONNECTION_GROUP'), (b'CREATE_USER', b'CREATE_USER'), (b'ADMINISTER', b'ADMINISTER')])),
            ],
            options={
                'db_table': 'guacamole_system_permission',
            },
        ),
        migrations.CreateModel(
            name='GuacamoleUser',
            fields=[
                ('user_id', models.AutoField(serialize=False, primary_key=True)),
                ('username', models.CharField(unique=True, max_length=128)),
                ('password_hash', models.BinaryField()),
                ('password_salt', models.BinaryField(null=True, blank=True)),
                ('disabled', models.BooleanField(default=False)),
                ('expired', models.BooleanField(default=False)),
                ('access_window_start', models.TimeField(null=True, blank=True)),
                ('access_window_end', models.TimeField(null=True, blank=True)),
                ('valid_from', models.DateField(null=True, blank=True)),
                ('valid_until', models.DateField(null=True, blank=True)),
                ('timezone', models.CharField(max_length=64, null=True, blank=True)),
                ('owner', models.ForeignKey(related_name='guacamole_user', to=settings.AUTH_USER_MODEL, null=True)),
            ],
            options={
                'db_table': 'guacamole_user',
            },
        ),
        migrations.CreateModel(
            name='GuacamoleUserPermission',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('permission', models.CharField(default=b'READ', max_length=128, choices=[(b'READ', b'READ'), (b'UPDATE', b'UPDATE'), (b'DELETE', b'DELETE'), (b'ADMINISTER', b'ADMINISTER')])),
                ('affected_user', models.ForeignKey(related_name='affected_perms', to='guac_auth.GuacamoleUser')),
                ('user', models.ForeignKey(related_name='owned_perms', to='guac_auth.GuacamoleUser')),
            ],
            options={
                'db_table': 'guacamole_user_permission',
            },
        ),
        migrations.AddField(
            model_name='guacamolesystempermission',
            name='user',
            field=models.ForeignKey(related_name='system_permissions', to='guac_auth.GuacamoleUser'),
        ),
        migrations.AddField(
            model_name='guacamoleconnectionpermission',
            name='user',
            field=models.ForeignKey(related_name='connection_permissions', to='guac_auth.GuacamoleUser'),
        ),
        migrations.AddField(
            model_name='guacamoleconnectionhistory',
            name='user',
            field=models.ForeignKey(related_name='history', to='guac_auth.GuacamoleUser'),
        ),
        migrations.AddField(
            model_name='guacamoleconnectiongrouppermission',
            name='user',
            field=models.ForeignKey(related_name='connection_group_permissions', to='guac_auth.GuacamoleUser'),
        ),
        migrations.AddField(
            model_name='guacamoleconnection',
            name='parent',
            field=models.ForeignKey(related_name='children', blank=True, to='guac_auth.GuacamoleConnectionGroup', null=True),
        ),
        migrations.AlterUniqueTogether(
            name='guacamoleuserpermission',
            unique_together=set([('user', 'affected_user', 'permission')]),
        ),
        migrations.AlterUniqueTogether(
            name='guacamolesystempermission',
            unique_together=set([('user', 'permission')]),
        ),
        migrations.AlterUniqueTogether(
            name='guacamoleconnectionpermission',
            unique_together=set([('user', 'connection', 'permission')]),
        ),
        migrations.AlterUniqueTogether(
            name='guacamoleconnectionparameter',
            unique_together=set([('connection', 'parameter_name')]),
        ),
        migrations.AlterUniqueTogether(
            name='guacamoleconnectiongrouppermission',
            unique_together=set([('user', 'connection_group', 'permission')]),
        ),
        migrations.AlterUniqueTogether(
            name='guacamoleconnectiongroup',
            unique_together=set([('connection_group_name', 'parent')]),
        ),
        migrations.AlterUniqueTogether(
            name='guacamoleconnection',
            unique_together=set([('connection_name', 'parent')]),
        ),
    ]
