from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User
from .models import UserProfile

# Mantener la configuración actual del admin para UserProfile
@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'credits')
    search_fields = ('user__username', 'user__email')

# Definir un inline admin descriptor para el modelo UserProfile
class UserProfileInline(admin.StackedInline):
    model = UserProfile
    can_delete = False
    verbose_name_plural = 'profiles'

# Definir una nueva clase UserAdmin que incluya el UserProfileInline
class UserAdmin(BaseUserAdmin):
    inlines = (UserProfileInline,)

# Re-registrar el modelo User utilizando el nuevo UserAdmin
admin.site.unregister(User)
admin.site.register(User, UserAdmin)
