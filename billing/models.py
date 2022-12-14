from email.policy import default
from msilib.schema import Class
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator
from django.contrib.auth.base_user import BaseUserManager
from django.utils.translation import gettext_lazy as _
from django.core.validators import FileExtensionValidator


def upload_directory_path(instance, filename):
    return 'UPLOADS/{0}/{1}'.format(instance.first_name, filename)


class CustomUserManager(BaseUserManager):

    def create_user(self, email, password=None, **extra_fields):

        if not email:
            raise ValueError('You must provide an email address')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password, **extra_fields):
        """
        Create and save a SuperUser with the given email and password.
        """
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError(_('Superuser must have is_staff=True.'))
        if extra_fields.get('is_superuser') is not True:
            raise ValueError(_('Superuser must have is_superuser=True.'))
        return self.create_user(email, password, **extra_fields)


class User(AbstractUser):
    is_admin = models.BooleanField(default=False)
    is_verified = models.BooleanField(default=False)
    email = models.EmailField(verbose_name='email address', unique=True)
    last_login = models.DateTimeField(null=True, blank=True)
    last_logout = models.DateTimeField(null=True, blank=True)
    username = None

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
        return self.email


class Admin(models.Model):

    gender_choices = (
        ('M', 'Male'),
        ('F', 'Female'),
        ('T', 'Transgender')
    )
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    phone_regex = RegexValidator(regex=r'^(?:(?:\+|0{0,2})91(\s*[\-]\s*)?|[0]?)?[789]\d{9}$',
                                 message="Phone number must be entered in the format: '+919999999999'. Up to 15 digits allowed.")
    phone_number = models.CharField(
        validators=[phone_regex], max_length=15, null=False, unique=True)
    gender = models.CharField(choices=gender_choices, max_length=2)
    email = models.EmailField(max_length=155, default=True)
    password = models.CharField(max_length=155, default=True)
    profile_image = models.ImageField(upload_to=upload_directory_path, blank=True, null=True, max_length=255, validators=[
                                      FileExtensionValidator(allowed_extensions=['pdf', 'jpg'])])

    def __str__(self):
        return self.first_name


class Main(models.Model):
    admin_id = models.CharField(max_length=255)
    main_title = models.CharField(max_length=255)
    description = models.CharField(max_length=255)

    def __str__(self):
        return self.main_title


class Sub_Title_One(models.Model):
    main = models.ForeignKey(
        Main, on_delete=models.CASCADE, related_name='sub_title_one')
    sub_title_one = models.CharField(max_length=255, blank=True)
    quantity = models.PositiveIntegerField()
    price = models.FloatField()
    description = models.CharField(max_length=255, blank=True)

    def __str__(self):
        return str(self.sub_title_one)


class Sub_Title_Two(models.Model):
    sub_title_one = models.ForeignKey(
        Sub_Title_One, on_delete=models.CASCADE, related_name='sub_title_two')
    sub_title_two = models.CharField(max_length=255, blank=True)
    quantity = models.PositiveIntegerField()
    price = models.FloatField()
    description = models.CharField(max_length=255, blank=True)

    def __str__(self):
        return str(self.sub_title_two)


def upload_directory_path(instance, filename):
    return 'PDF/{0}/{1}'.format(instance.storing_pdf, filename)


class StoringPDF(models.Model):
    storing_pdf = models.FileField(upload_to=upload_directory_path, blank=True, null=True, max_length=255, validators=[
        FileExtensionValidator(allowed_extensions=['pdf'])])


class Product(models.Model):
    product = models.ForeignKey(
        Main, on_delete=models.CASCADE, related_name='product')
    # description = models.CharField(max_length=255)

    def __str__(self):
        return str(self.product)


class Drafted(models.Model):
    drafted_product = models.OneToOneField(
        Main, on_delete=models.CASCADE, related_name='drafted')

    def __str__(self):
        return str(self.drafted_product)


class Pending(models.Model):
    pending_product = models.OneToOneField(
        Main, on_delete=models.CASCADE, related_name='pending')

    def __str__(self):
        return str(self.pending_product)


class Completed(models.Model):
    completed_product = models.OneToOneField(
        Main, on_delete=models.CASCADE, related_name='completed')

    def __str__(self):
        return str(self.completed_product)
