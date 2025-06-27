from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User, Group

class CustomUserAdmin(UserAdmin):
    list_display = ('username', 'email', 'first_name', 'last_name', 'is_staff', 'get_groups')
    list_filter = ('is_staff', 'is_superuser', 'groups')
    actions = ['make_author', 'make_editor']

    def get_groups(self, obj):
        return ", ".join([g.name for g in obj.groups.all()])
    get_groups.short_description = 'Groups'

    @admin.action(description='Make selected users Authors')
    def make_author(self, request, queryset):
        author_group = Group.objects.get(name='Authors')
        for user in queryset:
            user.groups.add(author_group)
    
    @admin.action(description='Make selected users Editors')
    def make_editor(self, request, queryset):
        editor_group = Group.objects.get(name='Editors')
        for user in queryset:
            user.groups.add(editor_group)

admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)