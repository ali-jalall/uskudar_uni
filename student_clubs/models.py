from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager


class UserAccountManager(BaseUserManager):
    def create_user(self, email, fullName, phone_number,
                    password=None, is_admin=False, is_club_manager=False, is_student=False, is_sks_admin=False):
        if not email:
            raise ValueError('User must have an email')
        
        email = self.normalize_email(email)
        email = email.lower()
        user = self.model(
            email=email,
            fullName=fullName,
            phone_number=phone_number,
            is_admin=is_admin,
            is_club_manager=is_club_manager,
            is_student=is_student,
            is_sks_admin=is_sks_admin
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, fullName, phone_number, password=None, is_sks_admin=False, **extra_fields):
        user = self.create_user(
            email=email,
            fullName=fullName,
            phone_number=phone_number,
            password=password,
            is_admin=True,
            is_sks_admin=is_sks_admin,
            **extra_fields
        )
        user.is_sks_admin = True  # Set this explicitly for superusers
        user.save(using=self._db)
        return user
    
class RedSeaUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(max_length=255, unique=True)
    fullName = models.CharField(max_length=255)
    phone_number = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    is_admin = models.BooleanField(default=False)
    is_student = models.BooleanField(default=False)
    is_club_manager = models.BooleanField(default=False)
    is_sks_admin = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    
    objects = UserAccountManager()
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['fullName', 'phone_number']

    def get_fullName(self):
        return self.fullName
    
    def check_student(self):
        return self.is_student
    
    def check_club_manager(self):
        return self.is_club_manager
    
    def check_sks_admin(self):
        return self.is_sks_admin

    def has_perm(self, perm, obj=None):
        return self.is_admin

    def has_module_perms(self, app_label):
        return True
    
    @property
    def is_staff(self):
        return self.is_admin

    class Meta:
        db_table="redseauser"

class Club(models.Model):
    club_id = models.AutoField(primary_key=True)
    club_name = models.CharField(max_length=255)
    club_manager = models.ManyToManyField(RedSeaUser)
    status_club = models.TextChoices("Active", "Not Active")
    date_created = models.DateTimeField(auto_now=True)
   

class Event(models.Model):
    event_id = models.AutoField(primary_key=True)
    event_name = models.CharField(max_length=255)
    event_type = models.CharField(max_length=255)
    event_date = models.DateTimeField()
    event_status = models.TextChoices("Approved", "Declined")
    event_hall = models.CharField(max_length=255)
    event_description = models.CharField(max_length=1000)
