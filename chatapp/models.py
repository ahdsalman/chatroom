
from django.db import models
from django.contrib.auth.models import BaseUserManager,AbstractBaseUser
import uuid
# Create your models here.
class Usermanager(BaseUserManager):
    def create_user(self,email,username,first_name=None,last_name=None,password=None):
        if not email:
            raise ValueError("User must have email Address")
        user = self.model(
            email=self.normalize_email(email),
            first_name = first_name,
            last_name = last_name,
            username = username
        )
        user.set_password(password)
        user.save(using=self._db)
        return user
    
    def create_superuser(self,email,username,password=None):
        user = self.create_user(
            email,
            username = username,
            password = password
        )
        user.is_admin = True
        user.save(using = self._db)
        return user
    

class User(AbstractBaseUser):
    email = models.EmailField(verbose_name="email_address",max_length=100,unique=True)
    first_name = models.CharField(max_length=100,null=True)
    last_name = models.CharField(max_length=100,null=True)
    username = models.CharField(max_length=100,unique=True)
    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    phone = models.CharField(max_length=13,null=True)
    image = models.ImageField(null=True)

    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)

    objects = Usermanager()

    USERNAME_FIELD="email"
    REQUIRED_FIELDS=["username","password"]

    
    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return self.is_admin

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True

    @property
    def is_staff(self):
        "Is the user a member of staff?"
        # Simplest possible answer: All admins are staff
        return self.is_admin
