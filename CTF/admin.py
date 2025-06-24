from django.contrib import admin
from .models import CustomeUser, Challenge, Hint, Submission, Category, ChallengeFile
from django.contrib.auth.admin import UserAdmin


class CustomUserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'points', 'is_active', 'is_staff')
    search_fields = ('username', 'email')
    list_filter = ('is_active', 'is_staff')
    
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Personal info', {'fields': ('first_name', 'last_name', 'email')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )

class ChallengeAdmin(admin.ModelAdmin):
    list_display = ('title', 'difficulty', 'categorie', 'point_val')
    search_fields = ('title', 'description')
    list_filter = ('difficulty', 'categorie')


class HintAdmin(admin.ModelAdmin):
    list_display = ('challenge', 'description')
    search_fields = ('description',)
    list_filter = ('challenge',)


class SubmissionAdmin(admin.ModelAdmin):
    list_display = ('user', 'challenge', 'end_time')
    search_fields = ('user__username', 'challenge__title')
    list_filter = ('end_time',)

admin.site.register(CustomeUser, CustomUserAdmin)
admin.site.register(Challenge, ChallengeAdmin)
admin.site.register(Hint, HintAdmin)
admin.site.register(Submission, SubmissionAdmin)
admin.site.register(Category)
admin.site.register(ChallengeFile)
