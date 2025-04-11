from flask_app import app
from flask_app.model.paises import Pais
from flask import render_template, request, flash, redirect
from flask_app.utils.decoradores import login_required
from flask import jsonify

@app.route("/paises")
@login_required
def listar_paises():

    datos = Pais.get_all()
    sujeto = "paises"

    return render_template("paises/listado.html", datos=datos, sujeto=sujeto)


@app.route("/paises/<id>")
@login_required
def detalle_pais(id):

    objeto = Pais.get(id)
    sujeto = "país"

    return render_template("paises/detalle.html", objeto=objeto, sujeto=sujeto)

# region CREAR
@app.route("/paises/crear")
@login_required
def pais_crear():
    return render_template("paises/formulario.html", sujeto='pais')


@app.route("/paises", methods=["POST"])
@login_required
def procesar_pais():
    print(request.form)
    datos = {
        'nombre': request.form['nombre']
    }

    Pais.save(datos)
    flash("Pais ingresado correctamente", "success")
    return redirect("/paises")
# endregion
# region EDITAR
@app.route("/paises/<int:id>/editar")
@login_required
def pais_actualizar(id):

    objeto = Pais.get(id)
    sujeto = "país"

    return render_template("paises/formulario_editar.html", sujeto=sujeto, objeto=objeto)


@app.route("/paises/<int:id>/editar", methods=["POST"])
@login_required
def procesar_editar(id):
    objeto = Pais.get(id)
    objeto.nombre = request.form['nombre']
    objeto.update()

    flash("Pais actualizado correctamente", "success")
    return redirect("/paises")
# endregion


@app.route("/paises/<int:id>/eliminar")
@login_required
def procesar_eliminado(id):

    Pais.delete(id)
    flash("Pais eliminado correctamente", "success")

    return redirect("/paises")

@app.route("/api/paises/<int:id>/eliminar")
@login_required
def procesar_eliminado_api(id):

    objeto = Pais.get(id)  
    resultado = Pais.delete(id)
    print("RESULTADO", resultado)

    if (resultado):
        return jsonify(ok=True, pais_eliminado=objeto.serializar())
    else:
        return jsonify(ok=False, mensaje="No se pudo eliminar el registro. Tiene asociados a otras filas.")
    



@app.route("/api/paises", methods=["POST"])
@login_required
def procesar_pais_api():
    print(request.json)
    
    datos = {
        'nombre': request.json['nombre']
    }

    id = Pais.save(datos)

    return jsonify(ok=True, id=id, mensaje="Creado exitosamente")