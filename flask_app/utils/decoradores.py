from flask import render_template, flash, redirect, session
from functools import wraps  

def login_required(funcion):
    @wraps(funcion)
    def wrapper(*args, **kwargs):
        if 'usuario' not in session:
            flash("No estás logeado", "error")
            return redirect("/login")
        return funcion(*args, **kwargs)
    return wrapper


def tiene_permiso(rol):
    def wrapper_permiso_main(funcion):
        @wraps(funcion)
        def wrapper_permiso(*args, **kwargs):
            
            if session['usuario']['rol'] != rol:
                flash("No eres admin", "error")
                return redirect("/")
            
            return funcion(*args, **kwargs)
        return wrapper_permiso
    return wrapper_permiso_main