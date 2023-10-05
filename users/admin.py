from django.contrib import admin

from users.models import User


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    moderator_fields_disable = ('email', 'phone', 'avatar', 'country', 'verification_token',
                                'is_staff', 'is_superuser', 'first_name', 'last_name', 'date_joined',
                                'groups', 'user_permissions', 'password', 'last_login')

    def get_readonly_fields(self, request, obj=None):
        if request.user.groups.filter(name='manager').exists():
            return self.moderator_fields_disable
        return super().get_readonly_fields(request, obj)
