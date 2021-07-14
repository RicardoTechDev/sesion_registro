from __future__ import unicode_literals
from django.db import models
import datetime, re

class  UserManager(models.Manager):
   def validador_basico(self, postData):
      
      EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
      SOLO_LETRAS = re.compile(r'^[a-zA-Z. ]+$')

      errors = {}

      if len(postData['firstname']) < 2:
         errors['firstname_len'] = "nombre debe tener al menos 2 caracteres de largo"

      if len(postData['lastname']) < 2:
         errors['lastname_len'] = "apellido debe tener al menos 2 caracteres de largo"

      if not EMAIL_REGEX.match(postData['email']):
         errors['email'] = "correo invalido"


      if not SOLO_LETRAS.match(postData['firstname']) or not SOLO_LETRAS.match(postData['lastname']):
         errors['solo_letras'] = "solo letras en nombre y apellido porfavor"

      
      if postData['birthday'] =="":
         errors['birthday'] = "debe ingresar la fecha de nacimiento"

      if len(postData['password']) < 8:
         errors['password'] = "contraseña debe tener al menos 8 caracteres"

      if postData['password'] != postData['password_check'] :
         errors['password_confirm'] = "las contraseña no son iguales."

         #hoy = datetime.date.today()
         #release =datetime.datetime.strptime(postData['release_date'], '%Y-%m-%d').date()
      return errors


class User(models.Model):
   firstname = models.CharField(max_length=100)
   lastname = models.CharField(max_length=100)
   email = models.CharField(max_length=255, unique=True)  #se puede usar models.EmailField
   password = models.CharField(max_length=70)
   birthday = models.DateField()
   rol = models.CharField(max_length=10, default='NORMAL')
   created_at = models.DateTimeField(auto_now_add=True)
   updated_at = models.DateTimeField(auto_now=True)
   objects = UserManager()

   def __str__(self):
      return f"{self.firstname} {self.lastname}"

   def __repr__(self):
      return f"{self.firstname} {self.lastname}"





#class Curso(models.Model):
   #nombre = models.CharField(max_length=255)
   #descripcion = models.ForeignKey(Descripcion, related_name='cursos', on_delete = models.CASCADE)
   #created_at = models.DateTimeField(auto_now_add=True)
   #updated_at = models.DateTimeField(auto_now=True)
   #objects = NOMBREManager()


#PARA MUCHOS A MUCHOS books = models.ManyToManyField(Book, related_name="publishers")

