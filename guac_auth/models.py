from django.db import models
from django.contrib.auth.models import User

from .fields import GuacamoleConnectionGroupTypeField
from .fields import GuacamoleObjectPermissionTypeField
from .fields import GuacamoleSystemPermissionTypeField

connection_group_type = (
    ('ORGANIZATIONAL', 'ORGANIZATIONAL'),
    ('BALANCING', 'BALANCING'))

object_permission_type = (
    ('READ', 'READ'),
    ('UPDATE', 'UPDATE'),
    ('DELETE', 'DELETE'),
    ('ADMINISTER', 'ADMINISTER'))

system_permission_type = (
    ('CREATE_CONNECTION', 'CREATE_CONNECTION'),
    ('CREATE_CONNECTION_GROUP', 'CREATE_CONNECTION_GROUP'),
    ('CREATE_USER', 'CREATE_USER'),
    ('ADMINISTER', 'ADMINISTER'))


class GuacamoleConnectionGroup(models.Model):
    connection_group_id = models.AutoField(primary_key=True)
    owner = models.ForeignKey(User, null=True)
    parent = models.ForeignKey(
        'self',
        related_name='child_groups',
        blank=True,
        null=True)
    connection_group_name = models.CharField(max_length=128)
    type = GuacamoleConnectionGroupTypeField(
        choices=connection_group_type,
        default='ORGANIZATIONAL')
    max_connections = models.IntegerField(blank=True, null=True)
    max_connections_per_user = models.IntegerField(blank=True, null=True)

    class Meta:
        db_table = 'guacamole_connection_group'
        unique_together = (('connection_group_name', 'parent'),)


class GuacamoleConnection(models.Model):
    connection_id = models.AutoField(primary_key=True)
    connection_name = models.CharField(max_length=128)
    parent = models.ForeignKey(
        GuacamoleConnectionGroup,
        related_name='children',
        blank=True,
        null=True)
    protocol = models.CharField(max_length=32)
    max_connections = models.IntegerField(blank=True, null=True)
    max_connections_per_user = models.IntegerField(blank=True, null=True)

    class Meta:
        db_table = 'guacamole_connection'
        unique_together = (('connection_name', 'parent'),)


class GuacamoleUser(models.Model):
    user_id = models.AutoField(primary_key=True)
    owner = models.ForeignKey(
        User,
        related_name='guacamole_user',
        null=True)
    username = models.CharField(unique=True, max_length=128)
    password_hash = models.BinaryField()
    password_salt = models.BinaryField(blank=True, null=True)
    disabled = models.BooleanField(default=False)
    expired = models.BooleanField(default=False)
    access_window_start = models.TimeField(blank=True, null=True)
    access_window_end = models.TimeField(blank=True, null=True)
    valid_from = models.DateField(blank=True, null=True)
    valid_until = models.DateField(blank=True, null=True)
    timezone = models.CharField(max_length=64, blank=True, null=True)

    class Meta:
        db_table = 'guacamole_user'


class GuacamoleConnectionGroupPermission(models.Model):
    user = models.ForeignKey(
        GuacamoleUser,
        related_name='connection_group_permissions')
    connection_group = models.ForeignKey(GuacamoleConnectionGroup)
    permission = GuacamoleObjectPermissionTypeField(
        choices=object_permission_type,
        default='READ')

    class Meta:
        db_table = 'guacamole_connection_group_permission'
        unique_together = (('user', 'connection_group', 'permission'),)


class GuacamoleConnectionHistory(models.Model):
    history_id = models.AutoField(primary_key=True)
    user = models.ForeignKey(
        GuacamoleUser,
        related_name='history')
    connection = models.ForeignKey(
        GuacamoleConnection,
        related_name='history')
    start_date = models.DateTimeField()
    end_date = models.DateTimeField(blank=True, null=True)

    class Meta:
        db_table = 'guacamole_connection_history'


class GuacamoleConnectionParameter(models.Model):
    connection = models.ForeignKey(
        GuacamoleConnection,
        related_name='parameters',
        on_delete=models.CASCADE)
    parameter_name = models.CharField(max_length=128)
    parameter_value = models.CharField(max_length=4096)

    class Meta:
        db_table = 'guacamole_connection_parameter'
        unique_together = (('connection', 'parameter_name'),)


class GuacamoleConnectionPermission(models.Model):
    user = models.ForeignKey(
        GuacamoleUser,
        related_name='connection_permissions',
        on_delete=models.CASCADE)
    connection = models.ForeignKey(
        GuacamoleConnection,
        related_name='connection_permissions',
        on_delete=models.CASCADE)
    permission = GuacamoleObjectPermissionTypeField(
        choices=object_permission_type,
        default='READ')

    class Meta:
        db_table = 'guacamole_connection_permission'
        unique_together = (('user', 'connection', 'permission'),)


class GuacamoleSystemPermission(models.Model):
    user = models.ForeignKey(
        GuacamoleUser,
        related_name='system_permissions')
    permission = GuacamoleSystemPermissionTypeField(
        choices=system_permission_type,
        default='CREATE_CONNECTION')

    class Meta:
        db_table = 'guacamole_system_permission'
        unique_together = (('user', 'permission'),)


class GuacamoleUserPermission(models.Model):
    user = models.ForeignKey(
        GuacamoleUser,
        related_name='owned_perms')
    affected_user = models.ForeignKey(
        GuacamoleUser,
        related_name='affected_perms')
    permission = GuacamoleObjectPermissionTypeField(
        choices=object_permission_type,
        default='READ')

    class Meta:
        db_table = 'guacamole_user_permission'
        unique_together = (('user', 'affected_user', 'permission'),)
