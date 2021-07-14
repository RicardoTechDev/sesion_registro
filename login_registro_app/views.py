from login_registro_app.models import User
from django.shortcuts import redirect, render, HttpResponse
from time import gmtime, strftime, localtime
from datetime import datetime
from django.contrib import messages
import bcrypt

def index(request):
    if 'usuario' not in request.session:
        return redirect("/login")

    context = {
        'saludo': 'Hola'
    }
    return render(request, 'index.html', context)


def logout(request):
    if 'usuario' in request.session:
        del request.session['usuario']
    
    return redirect("/login")

def login(request):
    if request.method == 'POST':
        print(request.POST)
        #buscamos el correo ingresado en la base de datos (si existe) y asignamos a la variable user
        user = User.objects.filter(email=request.POST['email_login'])
        
        if user: #una lista vacía devolverá falso
            #si existe tomamos el primer elemento de la lista user (devuelto por filter)
            log_user = user[0]

            #validamos la contraseña ingresada por el usuario 
            if bcrypt.checkpw(request.POST['password_login'].encode(), log_user.password.encode()):
                # si obtenemos True después de validar la contraseña, podemos poner la identificación del usuario en la sesión
                usuario = {
                    "id" : log_user.id,
                    "name" : f"{log_user}", # usamos el "def __str__(self)" definido en el modelo con return f"{self.firstname} {self.lastname}"
                    "email" : log_user.email,
                    "birthday" : log_user.birthday.strftime("%Y-%m-%d"),
                    "rol" : log_user.rol
                }

                request.session['usuario'] = usuario

                messages.success(request, "Logeado correctamente.")

                if request.session['usuario']['rol'] == "ADMIN" :
                    return redirect("/admin")
                
                else :
                    return redirect("/")

            else:#si la contraseña no coincide enviamos un mensaje de error al usuario
                messages.error(request, "Email o Contraseña invalidos.")
        
        else:#si la lista esta vacia significa que no se encontro el email ingresado
            #enviamos un mensaje de error al usuario
            messages.error(request, "Email o Contraseña invalidos.")

        return redirect("/login")#redirigimos al login


    else: #metodo GET
        return render(request, 'login.html')


def new_user (request):
    if request.method == 'POST':
        print(request.POST)
        #traemos el diccionario con errores para verificar si existen
        errors = User.objects.validador_basico(request.POST)
        print(errors)

        if len(errors) > 0:
            #si el diccionario de errores contiene algo, recorra cada par clave-valor y cree un mensaje flash
            for key, value in errors.items():
                messages.error(request, value);

                request.session['registro_firstname'] =  request.POST['firstname']
                request.session['registro_lastname'] =  request.POST['lastname']
                request.session['registro_email'] =  request.POST['email']
                request.session['registro_birthday'] =  request.POST['birthday']
                # redirigir al usuario al formulario para corregir los errores
                return redirect(f'login')

        else:
            # si el objeto de errores está vacío, eso significa que no hubo errores.

            request.session['registro_firstname'] = ""
            request.session['registro_lastname'] = ""
            request.session['registro_email'] = ""
            request.session['registro_birthday'] = ""

            #encriptación de la contraseña ingresada por el usuario
            password_encryp = bcrypt.hashpw(request.POST['password'].encode(), bcrypt.gensalt()).decode()

            new_user = User.objects.create(
                                            firstname = request.POST['firstname'],
                                            lastname = request.POST['lastname'],
                                            email = request.POST['email'],
                                            password = password_encryp,
                                            birthday = request.POST['birthday'],
                                            )
            usuario = {
                    "id" : new_user.id,
                    "name" : f"{new_user}", # usamos el "def __str__(self)" definido en el modelo con return f"{self.firstname} {self.lastname}"
                    "email" : new_user.email,
                    "birthday" : new_user.birthday,
                    "rol" : new_user.rol
                }
            request.session['usuario'] = usuario
            
            messages.success(request, f'Se realizado el registro con exito.')
            #redirigimos a la ruta según el rol del uuario
            if request.session['usuario']['rol'] == "ADMIN" :
                    return redirect("/admin")
                
            else :
                return redirect("/")

    if request.method == 'GET':
        context = {
                    'saludo': 'Hola'
                    }
        return render(request, 'registro.html', context)


def admin(request):
    if 'usuario' not in request.session:
        return redirect("/login")

    if request.session['usuario']['rol'] != 'ADMIN':
        messages.error(request, "Estimado usuario no tiene acceso permitido al área de administración.")
        return redirect("/")

    context = {
        'saludo': 'Hola'
    }
    return render(request, 'admin/index.html', context)