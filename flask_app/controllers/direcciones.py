from flask_app import app
from flask_app.model.direcciones import Direccion
from flask_app.model.comunas import Comuna
from flask import render_template, request, flash, redirect, session
from flask_app.utils.decoradores import login_required, tiene_permiso

@app.route("/direcciones")
@login_required
@tiene_permiso("normal")
def listar_direcciones():
    datos = Direccion.get_all_with_comuna()
    sujeto = "direcciones"
    return render_template("direcciones/listado.html", datos=datos, sujeto=sujeto)

@app.route("/direcciones/<id>")
@login_required
def detalle_direccion(id):

    objeto = Direccion.get(id)
    objeto.comuna = Comuna.get(objeto.comuna_id)
    sujeto = "direccion"
    return render_template("direcciones/detalle.html", objeto=objeto, sujeto=sujeto)

# region CREAR
@app.route("/direcciones/crear")
@login_required
def direccion_crear():
    comunas = Comuna.get_all()
    return render_template("direcciones/formulario.html", sujeto='direccion', comunas=comunas)

@app.route("/direcciones", methods=["POST"])
@login_required
def procesar_direccion():

    print("FORMULARIO", request.form)
    datos = {
        'calle': request.form['calle'],
        'numero': request.form['numero'],
        'comuna_id': request.form['comuna_id']
    }
    Direccion.save(datos)
    flash("Dirección ingresada correctamente", "success")
    return redirect("/direcciones")
# endregion

# region EDITAR
@app.route("/direcciones/<int:id>/editar")
@login_required
def direccion_actualizar(id):

    objeto = Direccion.get(id)
    sujeto = "direccion"
    comunas = Comuna.get_all()
    return render_template("direcciones/formulario_editar.html", sujeto=sujeto, objeto=objeto, comunas=comunas)

@app.route("/direcciones/<int:id>/editar", methods=["POST"])
@login_required
def procesar_editar_direccion(id):

    objeto = Direccion.get(id)
    objeto.calle = request.form['calle']
    objeto.numero = request.form['numero']
    objeto.comuna_id = request.form['comuna_id']
    objeto.update()
    flash("Dirección actualizada correctamente", "success")
    return redirect("/direcciones")
# endregion

@app.route("/direcciones/<int:id>/eliminar")
@login_required
def procesar_eliminado_direccion(id):

    Direccion.delete(id)
    flash("Dirección eliminada correctamente", "success")
    return redirect("/direcciones")
