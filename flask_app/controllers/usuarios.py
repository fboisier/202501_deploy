from flask_app import app
from flask_app.model.usuarios import Usuario
from flask_app.model.usuario_avanzado import UsuarioAvanzado
from flask import render_template, request, flash, redirect
from flask import jsonify

@app.route("/usuarios")
def listar_usuarios():

    usuarios = Usuario.get_all()

    return render_template("usuarios/usuarios.html", usuarios=usuarios)

@app.route("/api/prueba")
def prueba_api():

    data = {
        'nombre': 'Francisco',
        'edad': 40,
        'pasatiempos': ['programar', 'estudiar', 'videojuegos']
    }

    return jsonify(data)

@app.route("/api/usuarios")
def listar_usuarios_api():

    usuarios = Usuario.get_all()

    json_usuarios = []
    for usuario in usuarios:
        json_usuarios.append(usuario.serializar())

    return jsonify(usuarios=json_usuarios)

@app.route("/usuarios_avanzado")
def listar_usuarios_avanzado():

    usuarios = UsuarioAvanzado.get_all()

    return render_template("usuarios.html", usuarios=usuarios)

@app.route("/usuarios/<id>")
def detalle_usuario(id):

    usuario = Usuario.get(id)

    return render_template("usuarios/usuarios_detalle.html", usuario=usuario)



@app.route("/usuarios/crear")
def usuario_crear():
    return render_template("usuarios/formulario.html", sujeto='usuario')



@app.route("/usuarios", methods=["POST"])
def procesar_usuario():
    print(request.form)
    datos = {
        'nombre': request.form['nombre'],
        'email': request.form['email'],
        'contraseña': request.form['contraseña'],
    }

    Usuario.save(datos)
    flash("Usuario ingresado correctamente", "success")
    return redirect("/usuarios")


# region EDITAR
@app.route("/usuarios/<int:id>/editar")
def usuario_actualizar(id):

    objeto = Usuario.get(id)
    sujeto = "usuario"

    return render_template("usuarios/formulario_editar.html", sujeto=sujeto, objeto=objeto)


@app.route("/usuarios/<int:id>/editar", methods=["POST"])
def procesar_editar_usuario(id):
    print("formulario:", request.form)
    objeto = Usuario.get(id)
    objeto.nombre = request.form['nombre']
    objeto.email = request.form['email']
    objeto.contraseña = request.form['contraseña']
    objeto.update()

    flash("Usaurio actualizado correctamente", "success")
    return redirect("/usuarios")
# endregion

@app.route("/usuarios/<int:id>/eliminar")
def procesar_eliminado_usuario(id):

    Usuario.delete(id)
    flash("Usuario eliminado correctamente", "success")

    return redirect("/usuarios")


@app.route("/api/usuarios/<int:id>/eliminar")
def procesar_eliminado_usuario_api(id):
    
    objeto = Usuario.get(id)
    Usuario.delete(id)

    return jsonify(ok=True, usuario=objeto.serializar())