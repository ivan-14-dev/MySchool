# backend/apps/users/serializers.py
from rest_framework import serializers
from django.utils.translation import gettext_lazy as _
from .models import User, StudentProfile, TeacherProfile, ParentProfile, StudentParent

class UserSerializer(serializers.ModelSerializer):
    full_name = serializers.SerializerMethodField()
    
    class Meta:
        model = User
        fields = ('id', 'email', 'first_name', 'last_name', 'full_name',
                 'user_type', 'phone_number', 'date_of_birth', 'profile_picture',
                 'address', 'city', 'country', 'postal_code', 'is_verified',
                 'is_active', 'date_joined', 'last_login')
        read_only_fields = ('id', 'is_verified', 'is_active', 'date_joined', 'last_login')
    
    def get_full_name(self, obj):
        return obj.get_full_name()


class StudentProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    user_id = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.filter(user_type='student'), 
        source='user', write_only=True
    )
    
    class Meta:
        model = StudentProfile
        fields = '__all__'


class TeacherProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    user_id = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.filter(user_type='teacher'), 
        source='user', write_only=True
    )
    
    class Meta:
        model = TeacherProfile
        fields = '__all__'


class ParentProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    user_id = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.filter(user_type='parent'), 
        source='user', write_only=True
    )
    
    class Meta:
        model = ParentProfile
        fields = '__all__'


class StudentParentSerializer(serializers.ModelSerializer):
    student = UserSerializer(read_only=True)
    student_id = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.filter(user_type='student'), 
        source='student', write_only=True
    )
    parent = UserSerializer(read_only=True)
    parent_id = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.filter(user_type='parent'), 
        source='parent', write_only=True
    )
    
    class Meta:
        model = StudentParent
        fields = '__all__'