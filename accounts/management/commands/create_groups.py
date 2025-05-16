from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from accounts.models import User

class Command(BaseCommand):
    help = 'Creates default groups and assigns permissions'

    def handle(self, *args, **kwargs):
        # Create groups
        student_group, created = Group.objects.get_or_create(name='Students')
        faculty_group, created = Group.objects.get_or_create(name='Faculty')
        admin_group, created = Group.objects.get_or_create(name='Administrators')

        # Get content types
        user_content_type = ContentType.objects.get_for_model(User)

        # Get all permissions for User model
        user_permissions = Permission.objects.filter(content_type=user_content_type)

        # Assign permissions to groups
        # Students get basic permissions
        student_permissions = user_permissions.filter(codename__in=['view_user'])
        student_group.permissions.set(student_permissions)

        # Faculty get more permissions
        faculty_permissions = user_permissions.filter(codename__in=['view_user', 'change_user'])
        faculty_group.permissions.set(faculty_permissions)

        # Admins get all permissions
        admin_group.permissions.set(user_permissions)

        self.stdout.write(self.style.SUCCESS('Successfully created groups and assigned permissions')) 