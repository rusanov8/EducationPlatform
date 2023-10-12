from django.contrib import admin

from .models import User

# # Register your models here.
# admin.site.register(User)

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('id', 'email')

    list_filter = ('is_active', )

    search_fields = ('email', )
