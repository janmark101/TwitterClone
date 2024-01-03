from django.db import models
from django.contrib.auth.models import AbstractBaseUser,BaseUserManager
# Create your models here.

class UserManager(BaseUserManager):
    def create_user(self,email,username,password=None,staff=False,admin=False,active=True):
        if not email:
            raise ValueError("User must have an email address!")
        if not password:
            raise ValueError("User must have an password!")
        if not username:
            raise ValueError("User must have an username!")
        
        user_obj = self.model(
            email = self.normalize_email(email)
        )
        user_obj.set_password(password)
        user_obj.active = active
        user_obj.staff = staff
        user_obj.admin = admin
        user_obj.username = username
        user_obj.save(using=self._db)
        return user_obj
    
    def create_staffuser(self,email,username,password=None):
        staff_user = self.create_user(email=email,username=username,password=password,staff=True)
        return staff_user
    
    def create_superuser(self,email,username,password=None):
        super_user = self.create_user(email=email,username=username,password=password,staff=True,admin=True)
        return super_user
    

class User(AbstractBaseUser):
    email = models.EmailField(unique=True,null=False,max_length=100)
    username = models.CharField(unique=True,null=False,max_length=100)
    admin = models.BooleanField(default=False)
    staff = models.BooleanField(default=False)
    active = models.BooleanField(default=True)
    custom_name = models.CharField(unique=True,null=True,default='')
    description = models.TextField(null = True,max_length=400,default="No description.")
    date_created = models.DateTimeField(auto_now_add=True,null = False)
    following = models.ManyToManyField('self',  related_name='followers')
    is_premium = models.BooleanField(default=False)
    premium_expiration_date = models.DateField(null=True, blank=True)
    is_verified = models.BooleanField(default=False)
    verify_code = models.CharField(max_length=6,null=True,blank=True,unique=True)
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']
    
    objects = UserManager()
    
    def save(self, *args, **kwargs):
        if not self.custom_name:
            self.custom_name = self.username
        super().save(*args, **kwargs)


    def get_username(self):
        return self.username
    
    def __str__(self):
        return  self.email
    
    def has_perm(self,perm,obj=None):
        return True

    def has_module_perms(self,app_label):
        return True
    
    @property
    def is_active(self):
        return self.active
    
    @property
    def is_admin(self):
        return self.admin
    
    @property
    def is_staff(self):
        return self.staff