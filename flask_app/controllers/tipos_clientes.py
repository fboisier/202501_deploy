from flask_app import app
from flask_app.model.tipos_clientes import TipoCliente
from flask import render_template, request, flash, redirect

@app.route("/tipos_clientes")
def listar_tipos_clientes():
    datos = TipoCliente.get_all()
    sujeto = "tipos_clientes"
    return render_template("tipos_clientes/listado.html", datos=datos, sujeto=sujeto)

@app.route("/tipos_clientes/<id>")
def detalle_tipo_cliente(id):
    objeto = TipoCliente.get(id)
    sujeto = "tipo de cliente"
    return render_template("tipos_clientes/detalle.html", objeto=objeto, sujeto=sujeto)

# region CREAR
@app.route("/tipos_clientes/crear")
def tipo_cliente_crear():
    return render_template("tipos_clientes/formulario.html", sujeto='tipo de cliente')

@app.route("/tipos_clientes", methods=["POST"])
def procesar_tipo_cliente():
    datos = {
        'nombre': request.form['nombre']
    }
    TipoCliente.save(datos)
    flash("Tipo de cliente ingresado correctamente", "success")
    return redirect("/tipos_clientes")
# endregion

# region EDITAR
@app.route("/tipos_clientes/<int:id>/editar")
def tipo_cliente_actualizar(id):
    objeto = TipoCliente.get(id)
    sujeto = "tipo de cliente"
    return render_template("tipos_clientes/formulario_editar.html", sujeto=sujeto, objeto=objeto)

@app.route("/tipos_clientes/<int:id>/editar", methods=["POST"])
def procesar_editar_tipo_cliente(id):
    objeto = TipoCliente.get(id)
    objeto.nombre = request.form['nombre']
    objeto.update()
    flash("Tipo de cliente actualizado correctamente", "success")
    return redirect("/tipos_clientes")
# endregion

@app.route("/tipos_clientes/<int:id>/eliminar")
def procesar_eliminado_tipo_cliente(id):
    TipoCliente.delete(id)
    flash("Tipo de cliente eliminado correctamente", "success")
    return redirect("/tipos_clientes")
