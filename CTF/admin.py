from django.contrib import admin
from .models import CustomeUser, Challenge, Hint, Submission
from django.contrib.auth.admin import UserAdmin
# Register the CustomUser model
class CustomUserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'points', 'is_active', 'is_staff')
    search_fields = ('username', 'email')
    list_filter = ('is_active', 'is_staff')
    
    # Optional: You can also customize the form to include other fields or widgets
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Personal info', {'fields': ('first_name', 'last_name', 'email')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )

# Register the Challenge model
class ChallengeAdmin(admin.ModelAdmin):
    list_display = ('title', 'difficulty', 'categorie', 'point_val')
    search_fields = ('title', 'description')
    list_filter = ('difficulty', 'categorie')

# Register the Hint model
class HintAdmin(admin.ModelAdmin):
    list_display = ('challenge', 'description')
    search_fields = ('description',)
    list_filter = ('challenge',)

# Register the Submission model
class SubmissionAdmin(admin.ModelAdmin):
    list_display = ('user', 'challenge', 'end_time')
    search_fields = ('user__username', 'challenge__title')
    list_filter = ('end_time',)

# Registering models with admin
admin.site.register(CustomeUser, CustomUserAdmin)
admin.site.register(Challenge, ChallengeAdmin)
admin.site.register(Hint, HintAdmin)
admin.site.register(Submission, SubmissionAdmin)
