# admin.py
from django.contrib import admin
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import UserProfile, Shift

# Inline admin for UserProfile
class UserProfileInline(admin.StackedInline):
    model = UserProfile
    can_delete = False
    verbose_name_plural = "Profile"

# Extend the existing UserAdmin to include the profile inline
class UserAdmin(BaseUserAdmin):
    inlines = (UserProfileInline,)

# Unregister the default User admin and register the new one
admin.site.unregister(User)
admin.site.register(User, UserAdmin)

# Shift admin
@admin.register(Shift)
class ShiftAdmin(admin.ModelAdmin):
    list_display = ("user", "duty", "start_time", "end_time", "regular_move", "long_move", "pallet_return", "total_moves")
    readonly_fields = ("total_moves",)
    list_filter = ("duty", "user")


