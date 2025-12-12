from django.db import models
from django.contrib.auth.models import AbstractUser,BaseUserManager
from django.contrib.auth.hashers import make_password

class UserManager(BaseUserManager):
    def _create_user(self, email, password, **other_fields):
        """
        Create and save a user with the given email and password. And any other fields, if specified.
        """
        if not email:
            raise ValueError('An Email address must be set')
        email = self.normalize_email(email)
        
        user = self.model(email=email, **other_fields)
        user.password = make_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **other_fields):
        other_fields.setdefault('is_staff', False)
        other_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **other_fields)

    def create_superuser(self, email, password=None, **other_fields):
        other_fields.setdefault('is_staff', True)
        other_fields.setdefault('is_superuser', True)

        if other_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if other_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(email, password, **other_fields)
    

class User(AbstractUser):
    username=models.CharField(max_length=50,null=True,blank=True)
    first_name=models.CharField(max_length=50,null=True,blank=True)
    last_name=models.CharField(max_length=50,null=True,blank=True)
    email = models.EmailField(max_length=255, unique=True)
    mob=models.IntegerField(null=True)
    age=models.DateField(max_length=30,null=True)


    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['password']
    objects=UserManager()

    def get_username(self):
        return self.email 



class login(models.Model):
    email=models.EmailField(max_length=30,null=True)
    psswd=models.CharField(max_length=12,null=True)

class maincategory(models.Model):
    caname=models.CharField(max_length=40,null=True)
    price=models.IntegerField(null=True)
    valid=models.DateField(null=True)

    def __str__(self):
        return self.caname

class category(models.Model):
    cat=models.ForeignKey('maincategory', on_delete=models.CASCADE,null=True)
    cname=models.CharField(max_length=40,null=True)
    nos=models.IntegerField(null=True)
    valid=models.DateField(null=True)
    paid=models.BooleanField()
    image=models.ImageField(upload_to='image/',null=True)
    def __str__(self):
        return self.cname

class program(models.Model):
    title=models.CharField(max_length=40,null=True)
    Episode=models.IntegerField(null=True)
    videourl=models.CharField(max_length=40,null=True)
    image=models.ImageField(upload_to='image/',null=True)
    video=models.FileField(upload_to='video/',null=True)
    ca=models.ForeignKey('category', on_delete=models.CASCADE,null=True)
    def __str__(self):
        return self.title

class order(models.Model):
    ct=models.ForeignKey('maincategory', on_delete=models.CASCADE,null=True)
    us=models.ForeignKey('User', on_delete=models.CASCADE,null=True)
    price=models.IntegerField(null=True)
    validity=models.DateField(null=True)
    date=models.DateField(null=True)
    def __str__(self):
        return str(self.ct)
        