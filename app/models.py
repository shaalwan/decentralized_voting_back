from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import MinLengthValidator,MaxLengthValidator
from django.contrib.auth.models import UserManager as BaseUserManager



class UserManager(BaseUserManager):
    """ User Manager that knows how to create users via email instead of username """
    def _create_user(self, email, password, **extra_fields):
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email=None, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        return self._create_user(email, password, **extra_fields)

    def create_user(self, email=None, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", False)
        extra_fields.setdefault("is_superuser", False)
        return self._create_user(email, password, **extra_fields)


# Create your models here.
class User(AbstractUser):
  objects = UserManager() 
  username = None
  USERNAME_FIELD = 'email'
  email = models.EmailField(unique = True)
  password = models.CharField(blank=False,null =False,max_length=100)
  is_company = models.BooleanField(default = False)
  REQUIRED_FIELDS = []

class Voter(models.Model):
  user = models.ForeignKey(User,on_delete=models.CASCADE)
  aadhar = models.BigIntegerField(validators=[MaxLengthValidator(1000000000000000),MinLengthValidator(9999999999999999)],unique= True)
  election_address =  models.CharField(max_length=256,blank = False,null = False)
  class Meta:
    unique_together = ('user', 'election_address',)

class Election(models.Model):
    election = models.TextField()
    user = models.ForeignKey(User,on_delete=models.CASCADE)