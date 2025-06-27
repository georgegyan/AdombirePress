from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from blog.models import Post

class Command(BaseCommand):
    help = 'Creates default user groups with permissions'

    def handle(self, *args, **options):
        # Create or get groups
        author_group, created = Group.objects.get_or_create(name='Authors')
        editor_group, created = Group.objects.get_or_create(name='Editors')
        admin_group, created = Group.objects.get_or_create(name='Admins')

        # Get content type for Post model
        content_type = ContentType.objects.get_for_model(Post)

        # Get permissions
        add_post = Permission.objects.get(codename='add_post', content_type=content_type)
        change_post = Permission.objects.get(codename='change_post', content_type=content_type)
        delete_post = Permission.objects.get(codename='delete_post', content_type=content_type)
        can_publish = Permission.objects.get(codename='can_publish_post', content_type=content_type)
        can_edit_all = Permission.objects.get(codename='can_edit_all_posts', content_type=content_type)
        can_delete_all = Permission.objects.get(codename='can_delete_all_posts', content_type=content_type)

        # Assign permissions to Authors
        author_group.permissions.add(add_post, change_post, delete_post)
        
        # Assign permissions to Editors
        editor_group.permissions.add(
            add_post, change_post, delete_post, 
            can_publish, can_edit_all, can_delete_all
        )
        
        # Assign all permissions to Admins
        admin_group.permissions.add(*Permission.objects.all())

        self.stdout.write(self.style.SUCCESS('Successfully created groups and assigned permissions'))