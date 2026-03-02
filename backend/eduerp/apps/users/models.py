from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _
from django.core.validators import RegexValidator

class User(AbstractUser):
    USER_TYPE_CHOICES = (
        ('admin', _('Administrator')),
        ('teacher', _('Teacher')),
        ('student', _('Student')),
        ('parent', _('Parent')),
        ('staff', _('Staff')),
    )
    
    user_type = models.CharField(_("user type"), max_length=10, choices=USER_TYPE_CHOICES)
    # Utiliser une chaîne pour la référence au lieu d'importer directement
    school = models.ForeignKey('core.School', on_delete=models.CASCADE, related_name='users', null=True, blank=True)
    phone_regex = RegexValidator(
        regex=r'^\+?1?\d{9,15}$',
        message=_("Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed.")
    )
    phone_number = models.CharField(_("phone number"), validators=[phone_regex], max_length=17, blank=True)
    date_of_birth = models.DateField(_("date of birth"), null=True, blank=True)
    profile_picture = models.ImageField(_("profile picture"), upload_to='profiles/', blank=True, null=True)
    address = models.TextField(_("address"), blank=True, null=True)
    city = models.CharField(_("city"), max_length=100, blank=True, null=True)
    country = models.CharField(_("country"), max_length=100, default="France", blank=True, null=True)
    postal_code = models.CharField(_("postal code"), max_length=20, blank=True, null=True)
    is_verified = models.BooleanField(_("verified"), default=False)
    verification_token = models.CharField(_("verification token"), max_length=100, blank=True, null=True)
    
    # Additional fields for parents
    emergency_contact = models.CharField(_("emergency contact"), max_length=255, blank=True, null=True)
    emergency_phone = models.CharField(_("emergency phone"), validators=[phone_regex], max_length=17, blank=True)
    
    # Relations many-to-many pour les permissions personnalisées
    custom_permissions = models.ManyToManyField(
        'auth.Permission',
        verbose_name=_('custom permissions'),
        blank=True,
        related_name='custom_user_set',
        related_query_name='custom_user'
    )
    
    class Meta:
        verbose_name = _("user")
        verbose_name_plural = _("users")
        ordering = ['last_name', 'first_name']

    def __str__(self):
        return f"{self.get_full_name()} ({self.get_user_type_display()})"

    def has_perm(self, perm, obj=None):
        # Vérifier les permissions personnalisées
        if self.custom_permissions.filter(codename=perm).exists():
            return True
        
        # Vérifier les permissions Django standard
        return super().has_perm(perm, obj)
    
    def has_perms(self, perm_list, obj=None):
        return all(self.has_perm(perm, obj) for perm in perm_list)

# Les autres modèles User doivent également utiliser des références en chaîne
class StudentProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='student_profile')
    student_id = models.CharField(_("student ID"), max_length=50, unique=True)
    admission_date = models.DateField(_("admission date"))
    graduation_date = models.DateField(_("graduation date"), null=True, blank=True)
    class_level = models.CharField(_("class level"), max_length=50)
    section = models.CharField(_("section"), max_length=50, blank=True, null=True)
    roll_number = models.IntegerField(_("roll number"))
    house = models.CharField(_("house"), max_length=50, blank=True, null=True)
    blood_group = models.CharField(_("blood group"), max_length=5, blank=True, null=True)
    allergies = models.TextField(_("allergies"), blank=True, null=True)
    medical_conditions = models.TextField(_("medical conditions"), blank=True, null=True)
    previous_school = models.CharField(_("previous school"), max_length=255, blank=True, null=True)
    created_at = models.DateTimeField(_("created at"), auto_now_add=True)
    updated_at = models.DateTimeField(_("updated at"), auto_now=True)
    
    
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, 
                                 related_name='studentprofile_created')
    updated_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, 
                                 related_name='studentprofile_updated')
    
    class Meta:
        verbose_name = _("student profile")
        verbose_name_plural = _("student profiles")
        ordering = ['class_level', 'roll_number']

    def __str__(self):
        return f"{self.user.get_full_name()} - {self.student_id}"

class TeacherProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='teacher_profile')
    teacher_id = models.CharField(_("teacher ID"), max_length=50, unique=True)
    department = models.ForeignKey('core.Department', on_delete=models.SET_NULL, null=True, 
                                 related_name='teachers')
    hire_date = models.DateField(_("hire date"))
    qualification = models.CharField(_("qualification"), max_length=255)
    specialization = models.CharField(_("specialization"), max_length=255, blank=True, null=True)
    years_of_experience = models.IntegerField(_("years of experience"), default=0)
    is_class_teacher = models.BooleanField(_("class teacher"), default=False)
    bio = models.TextField(_("bio"), blank=True, null=True)
    created_at = models.DateTimeField(_("created at"), auto_now_add=True)
    updated_at = models.DateTimeField(_("updated at"), auto_now=True)

    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, 
                                 related_name='teacherprofile_created')
    updated_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, 
                                 related_name='teacherprofile_updated')
    
    class Meta:
        verbose_name = _("teacher profile")
        verbose_name_plural = _("teacher profiles")
        ordering = ['user__last_name', 'user__first_name']

    def __str__(self):
        return f"{self.user.get_full_name()} - {self.teacher_id}"

class ParentProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='parent_profile')
    occupation = models.CharField(_("occupation"), max_length=255, blank=True, null=True)
    employer = models.CharField(_("employer"), max_length=255, blank=True, null=True)
    relationship = models.CharField(_("relationship"), max_length=50, 
                                  choices=[('father', _('Father')), ('mother', _('Mother')), 
                                           ('guardian', _('Guardian'))])
    created_at = models.DateTimeField(_("created at"), auto_now_add=True)
    updated_at = models.DateTimeField(_("updated at"), auto_now=True)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, 
                                 related_name='parentprofile_created')
    updated_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, 
                                 related_name='parentprofile_updated')
    
    class Meta:
        verbose_name = _("parent profile")
        verbose_name_plural = _("parent profiles")

    def __str__(self):
        return f"{self.user.get_full_name()} ({self.relationship})"

class StudentParent(models.Model):
    student = models.ForeignKey('User', on_delete=models.CASCADE, 
                              limit_choices_to={'user_type': 'student'},
                              related_name='parents')
    parent = models.ForeignKey('User', on_delete=models.CASCADE, 
                             limit_choices_to={'user_type': 'parent'},
                             related_name='students')
    relationship = models.CharField(_("relationship"), max_length=50, 
                                  choices=[('father', _('Father')), ('mother', _('Mother')), 
                                           ('guardian', _('Guardian'))])
    is_primary = models.BooleanField(_("primary contact"), default=False)
    
    class Meta:
        verbose_name = _("student parent")
        verbose_name_plural = _("student parents")
        constraints = [
        models.UniqueConstraint(fields=['student', 'parent'], name='unique_student_parent')
        ]

    def __str__(self):
        return f"{self.parent.get_full_name()} -> {self.student.get_full_name()}"