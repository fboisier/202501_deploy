from flask_app import app
from flask_app.model.clientes import Cliente
from flask_app.model.direcciones import Direccion
from flask_app.model.tipos_clientes import TipoCliente
from flask_app.model.productos import Producto

from flask import render_template, request, flash, redirect

@app.route("/clientes")
def listar_clientes():
    datos = Cliente.get_all()
    sujeto = "clientes"
    return render_template("clientes/listado.html", datos=datos, sujeto=sujeto)

@app.route("/clientes/<id>")
def detalle_cliente(id):
    objeto = Cliente.get(id)
    if objeto:
        objeto.direccion = Direccion.get(objeto.direccion_id)
        objeto.tipo_cliente = TipoCliente.get(objeto.tipo_cliente_id)
        sujeto = "cliente"
        return render_template("clientes/detalle.html", objeto=objeto, sujeto=sujeto)
    flash("Cliente no encontrado", "error")
    return redirect("/clientes")

# region CREAR
@app.route("/clientes/crear")
def cliente_crear():
    direcciones = Direccion.get_all_with_comuna()
    tipos_cliente = TipoCliente.get_all()
    return render_template("clientes/formulario.html", sujeto='cliente', direcciones=direcciones, tipos_cliente=tipos_cliente)

@app.route("/clientes", methods=["POST"])
def procesar_cliente():
    datos = {
        'dni': request.form['dni'],
        'nombre': request.form['nombre'],
        'apellido': request.form['apellido'],
        'direccion_id': request.form['direccion_id'],
        'tipo_cliente_id': request.form['tipo_cliente_id']
    }
    if not Cliente.validar(datos):
        return redirect("/clientes/crear")

    Cliente.save(datos)
    flash("Cliente ingresado correctamente", "success")
    return redirect("/clientes")
# endregion

# region EDITAR
@app.route("/clientes/<int:id>/editar")
def cliente_actualizar(id):
    objeto = Cliente.get(id)
    if not objeto:
        flash("Cliente no encontrado", "error")
        return redirect("/clientes")
        
    sujeto = "cliente"
    direcciones = Direccion.get_all_with_comuna()
    tipos_cliente = TipoCliente.get_all()
    return render_template("clientes/formulario_editar.html", sujeto=sujeto, objeto=objeto, direcciones=direcciones, tipos_cliente=tipos_cliente)

@app.route("/clientes/<int:id>/editar", methods=["POST"])
def procesar_editar_cliente(id):
    objeto = Cliente.get(id)
    if not objeto:
        flash("Cliente no encontrado", "error")
        return redirect("/clientes")
        
    objeto.dni = request.form['dni']
    objeto.nombre = request.form['nombre']
    objeto.apellido = request.form['apellido']
    objeto.direccion_id = request.form['direccion_id']
    objeto.tipo_cliente_id = request.form['tipo_cliente_id']
    objeto.update()
    flash("Cliente actualizado correctamente", "success")
    return redirect("/clientes")
# endregion

@app.route("/clientes/<int:id>/eliminar")
def procesar_eliminado_cliente(id):
    if Cliente.delete(id):
        flash("Cliente eliminado correctamente", "success")
    else:
        flash("Error al eliminar el cliente", "error")
    return redirect("/clientes")


@app.route("/clientes/<int:id>/productos/crear")
def producto_en_cliente(id):
    objeto = Cliente.get(id)
    productos = Producto.get_all()
    return render_template("clientes/formulario_producto.html", objeto=objeto, productos=productos)

@app.route("/clientes/<int:id>/productos/crear", methods=["POST"])
def procesar_producto_en_cliente(id):
    cliente_instancia = Cliente.get(id)
    producto_id = request.form['producto_id']

    cliente_instancia.save_producto(producto_id)
    flash("Producto agregado al cliente correctamente", "success")
    return redirect(f"/clientes/{id}")