from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models
from django.contrib.auth import get_user_model

class UserManager(BaseUserManager):
    def create_user(self, nombre, apellido, correo, password = None, profesor = False, admin = False):
        if not nombre:
            raise ValueError("Los usuarios deben tener un nombre")
        if not apellido:
            raise ValueError("Los usuarios deben tener un apellido")
        if not correo:
            raise ValueError("Los usuarios deben tener un correo")
        if not password:
            raise ValueError("Los usuarios deben tener un correo")


        user_obj = self.model(correo = self.normalize_email(correo))
        #user_obj= get_user_model().objects.create_user(correo = self.normalize_email(correo))
        
        user_obj.nombre = nombre
        user_obj.apellido = apellido
        user_obj.evaluador = True
        user_obj.profesor = profesor
        user_obj.admin = admin
        user_obj.set_password(password)
        user_obj.save()
        #user_obj.save(using = self._db)
        return user_obj

    def create_profesor_user(self, nombre, apellido, correo, password = None):
        user = self.create_user(nombre,apellido,correo,password,profesor = True)
        return user

    def create_superuser(self,nombre,apellido,correo,password = None):
        user = self.create_user(nombre,apellido,correo,password,profesor = True, admin=True)
        return user
        
    
        
# Create your models here.
class CustomUser(AbstractBaseUser, PermissionsMixin):
    correo = models.EmailField(unique = True)
    nombre = models.CharField(max_length=80)
    apellido = models.CharField(max_length=80)

    evaluador = models.BooleanField(default=False)
    profesor = models.BooleanField(default=False)
    admin = models.BooleanField(default = False)

    USERNAME_FIELD = 'correo'

    REQUIRED_FIELDS = ['nombre','apellido']
    objects = UserManager()

    def __str__(self):
        return self.correo

    def get_nombre(self):
        return self.nombre

    def get_apellido(self):
        return self.apellido

    @property
    def is_evaluador(self):
        return self.evaluador

    @property 
    def is_profesor(self):
        return self.profesor

    @property
    def is_admin(self):
        return self.admin

    @property
    def is_staff(self):
        return self.admin
    
    @property
    def is_superuser(self):
        return self.admin