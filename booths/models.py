from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.contrib.auth.models import User

# class CustomUserManager(BaseUserManager):
#     def create_user(self, email, username, password=None):
#         if not email:
#             raise ValueError('User must have email')
#         if not username:
#             raise ValueError('User must have username')

#         user = self.create_user(
#             email=self.normalize_email(email),
#             username=username,
#         )

#         user.set_password(password)
#         user.save(using=self._db)
#         return user


#     def create_superuser(self, email, username, password):
#         user = self.create_user(
#             email=self.normalize_email(email),
#             username=username,
#             password=password,
#         )

#         user.is_admin = True
#         user.is_staff = True
#         user.is_superuser = True
#         user.save(using=self._db)

#         return user

    
class CustomUserManager(BaseUserManager):
    '''For authentication use email instead of username'''
    def _create_user(self, email, password, **extra_fields):
        '''Create and save user with the given email and password'''
        if not email:
            raise ValueError('The email must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_user(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        '''Create and save a superuser with given email and password'''
        # extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_admin', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True')
        if extra_fields.get('is_admin') is not True:
            raise ValueError('Superuser must have is_admin=True')
        return self._create_user(email, password, **extra_fields)


class CustomUser(AbstractBaseUser):
    email           = models.EmailField(verbose_name='email', max_length=254, unique=True)
    username        = models.CharField(verbose_name='username', max_length=11, unique=True)
    date_joined     = models.DateTimeField(auto_now_add=True)
    last_login      = models.DateTimeField(auto_now_add=True, auto_now=False)
    is_admin        = models.BooleanField(default=False)
    is_active       = models.BooleanField(default=True)
    is_staff        = models.BooleanField(default=False)
    is_superuser    = models.BooleanField(default=False)

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']

    objects = CustomUserManager()

    def __str__(self):
        return f'{self.username} {self.email}'

    def has_perm(self, perm, obj=None):
        return self.is_admin

    def has_module_perms(self, app_label):
        return True

    class Meta:
        verbose_name = 'User'



class Faculty(models.Model):
    name = models.CharField(verbose_name="Faculty Name", unique=True, max_length=100)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = 'Faculties'
    

class Department(models.Model):
    name        = models.CharField(verbose_name="Department Name", unique=True, max_length=100)
    faculty     = models.ForeignKey(Faculty, on_delete=models.CASCADE)

    def __str__(self):
        return self.name
    

class Student(models.Model):
    '''Holds all student details'''
    matric_number   = models.CharField(max_length=11)
    first_name      = models.CharField(max_length=50)
    middle_name     = models.CharField(max_length=50, null=True)
    last_name       = models.CharField(max_length=50, help_text='Surname')
    avater          = models.ImageField(verbose_name="passport", upload_to='images/', null=True, blank=True)
    department      = models.ForeignKey(Department, on_delete=models.CASCADE)
    
    def __str__(self):
        return f'{self.last_name}, {self.first_name} {self.middle_name} {self.matric_number}' 
    


class Session(models.Model):
    '''This define the session the votes occurred'''
    name = models.CharField(verbose_name="Session", unique=True, max_length=9)

    def __str__(self):
        return self.name
    

class Position(models.Model):
    '''Defines available positions'''
    name = models.CharField(verbose_name="Title", max_length=50)
    description = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.name


class Choice(models.Model):
    '''This hold the candidates to be voted for'''
    position    = models.ForeignKey(Position, on_delete=models.CASCADE)
    # poll        = models.ForeignKey(Poll, on_delete=models.CASCADE)
    candidate   = models.ForeignKey(Student, on_delete=models.CASCADE)
    description = models.TextField(null=True, blank=True )
    number_of_vote = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f'{self.candidate} {self.position}'
    
    
class Vote(models.Model):
    '''This hold candidates votes'''
    choice  = models.ForeignKey(Choice, on_delete=models.CASCADE)
    voter   = models.ForeignKey(Student, on_delete=models.CASCADE)
    # poll    = models.ForeignKey(Poll, on_delete=models.CASCADE)
    
    # def __str__(self):
    #     return self.choice.candidate.first_name
    

    
