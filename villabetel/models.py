import random
import string

from django.contrib.auth.models import (AbstractBaseUser, BaseUserManager,
                                        PermissionsMixin)
from django.db import models
from django.urls import reverse
from django.utils import timezone
from django.utils.text import slugify
from django.utils.translation import gettext_lazy as _



def rand_slug():
    return ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(6))


class CustomAccountManager(BaseUserManager):
    def create_user(self, email, first_name, last_name, password, **other_fields):

        if not email:
            raise ValueError(_('You must provide an email address'))

        email = self.normalize_email(email)
        user = self.model(email=email, first_name=first_name,
                          last_name=last_name, **other_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, first_name, last_name, password, **other_fields):

        other_fields.setdefault('is_staff', True)
        other_fields.setdefault('is_superuser', True)
        other_fields.setdefault('is_active', True)

        if other_fields.get('is_staff') is not True:
            raise ValueError(
                'Superuser must be assigned to is_staff=True.')
        if other_fields.get('is_superuser') is not True:
            raise ValueError(
                'Superuser must be assigned to is_superuser=True.')

        return self.create_user(email, first_name, last_name, password, **other_fields)


class UserProfile(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(_('email address'), unique=True)
    first_name = models.CharField(max_length=100,verbose_name='Nombre')
    last_name = models.CharField(max_length=100,verbose_name='Apellido')
    document_number = models.CharField(max_length=20, blank=True, null=True,verbose_name='Documento')
    profile_pic = models.ImageField(
        upload_to='users/', default='users/default.png')
    followers = models.ManyToManyField(
        "self",
        related_name='following',
        symmetrical=False,
        blank=True)
    slug = models.SlugField(max_length=255, unique=True)

    register_date = models.DateTimeField(default=timezone.now)

    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)

    objects = CustomAccountManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']

    def __str__(self):
        return f'{self.first_name} {self.last_name}'

    def get_absolute_url(self):
        return reverse('users:user_detail', args=[self.slug])

    def count_following(self):
        users_following = UserProfile.objects.filter(followers=self)
        return users_following.count()

    def is_follower(self, other_user):
        if other_user in self.followers.all():
            return True
        return False

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(rand_slug() + "-" + self.email)
        super(UserProfile, self).save(*args, **kwargs)
        
class Category(models.Model):
    name = models.CharField(max_length=100, verbose_name='Nombre')

    def __str__(self):
        return self.name

class Product(models.Model):
    name = models.CharField(max_length=200, verbose_name='Nombre')
    description = models.TextField(verbose_name='Descripcion')
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Precio')
    category = models.ForeignKey(Category, verbose_name='Categoria', on_delete=models.CASCADE)

    def __str__(self):
        return self.name
    
class Area(models.Model):
    name = models.CharField(max_length=100, verbose_name='Nombre')

    def __str__(self):
        return self.name
    
class Table(models.Model):
    number = models.IntegerField(verbose_name='Número')
    area = models.ForeignKey(Area, verbose_name='Zona', on_delete=models.CASCADE)

    def __str__(self):
        return str(self.number)
    
class Waiter(models.Model):
    user_profile = models.OneToOneField(UserProfile, on_delete=models.CASCADE)
    nickname = models.CharField(max_length=100, verbose_name='Nickname')

    def __str__(self):
        return f'{self.nickname} ({self.user_profile.first_name} {self.user_profile.last_name})'

class Account(models.Model):
    table = models.ForeignKey(Table, on_delete=models.CASCADE)
    waiter = models.ForeignKey(Waiter, on_delete=models.CASCADE)
    ammount = models.PositiveIntegerField(null=True, blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    state = models.CharField(max_length=20)
    timestamp = models.DateTimeField(auto_now_add=True)


class ProductQuantity(models.Model):
    account = models.ForeignKey(Account, on_delete=models.CASCADE, related_name='product_quantities')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()


class Invoice(models.Model):
    table = models.ForeignKey(Table, on_delete=models.CASCADE)
    account = models.ManyToManyField(Account)
    total = models.IntegerField()
    state = models.CharField(max_length=20)  # Pendiente, Pagada, etc.
    timestamp = models.DateTimeField(auto_now_add=True)

