from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User, StudentProfile, TeacherProfile, ParentProfile, StudentParent

@admin.register(User)
class UserAdmin(BaseUserAdmin):
    list_display = ('username', 'email', 'first_name', 'last_name', 'user_type', 'is_staff', 'is_superuser', 'is_active')
    list_filter = ('user_type', 'is_staff', 'is_superuser', 'is_active')
    fieldsets = BaseUserAdmin.fieldsets + (
        ('Type utilisateur', {'fields': ('user_type', 'phone_number', 'address', 'date_of_birth', 'profile_picture', 'emergency_contact', 'emergency_phone')}),
    )
    add_fieldsets = BaseUserAdmin.add_fieldsets + (
        ('Type utilisateur', {'fields': ('user_type', 'phone_number', 'email')}),
    )
    search_fields = ('username', 'email', 'first_name', 'last_name')

@admin.register(StudentProfile)
class StudentProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'student_id', 'class_level', 'roll_number')
    search_fields = ('user__first_name', 'user__last_name', 'student_id')
    raw_id_fields = ('user',)

@admin.register(TeacherProfile)
class TeacherProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'teacher_id', 'qualification')
    search_fields = ('user__first_name', 'user__last_name', 'employee_id')
    raw_id_fields = ('user',)

@admin.register(ParentProfile)
class ParentProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'occupation')
    search_fields = ('user__first_name', 'user__last_name')
    raw_id_fields = ('user',)

@admin.register(StudentParent)
class StudentParentAdmin(admin.ModelAdmin):
    list_display = ('student', 'parent', 'relationship')
    list_filter = ('relationship',)
    raw_id_fields = ('student', 'parent',)
