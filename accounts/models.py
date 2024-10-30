from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from base.models import Company

class MyUserManager(BaseUserManager):
    def create_user(self, email, first_name, last_name, is_driver, is_dispatcher, company, password=None):
        if not email:
            raise ValueError("Users must have an email address")

        user = self.model(
            email = self.normalize_email(email),
            first_name = first_name,
            last_name = last_name,
            company = company,
            is_dispatcher=is_dispatcher,
            is_driver=is_driver,
        )

        user.set_password(password)
        user.save(using=self._db)

        if is_driver:
            Driver.objects.create(user=user)
        elif is_dispatcher:
            Dispatcher.objects.create(user=user)
    

        return user
    
    def create_superuser(self, email, first_name, last_name, password=None):
        
        user = self.create_user(
            email,
            first_name = first_name,
            last_name = last_name,
            password = password,
            company=None
        )

        user.is_admin = True
        user.save(using=self._db)
        return user
    
class User(AbstractBaseUser):
    email = models.EmailField(
        verbose_name="email address",
        max_length=255,
        unique=True,
    )
    first_name = models.CharField(max_length=100, blank=False)
    last_name = models.CharField(max_length=100, blank=False)
    is_active = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)
    is_dispatcher = models.BooleanField(default=False)
    is_driver = models.BooleanField(default=False)
    company = models.ForeignKey(Company, on_delete=models.CASCADE)


    objects = MyUserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["first_name", "last_name", "company", "is_dispatcher", "is_driver"]

class Dispatcher(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="dispatcher")

class Driver(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="driver")