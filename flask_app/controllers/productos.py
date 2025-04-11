from flask_app import app
from flask_app.model.productos import Producto
from flask import render_template, request, flash, redirect

@app.route("/productos")
def listar_productos():

    datos = Producto.get_all()
    sujeto = "productos"

    return render_template("productos/listado.html", datos=datos, sujeto=sujeto)


@app.route("/productos/<id>")
def detalle_producto(id):

    objeto = Producto.get(id)
    sujeto = "producto"

    return render_template("productos/detalle.html", objeto=objeto, sujeto=sujeto)

# region CREAR
@app.route("/productos/crear")
def producto_crear():
    return render_template("productos/formulario.html", sujeto='producto')


@app.route("/productos", methods=["POST"])
def procesar_producto():
    print(request.form)
    datos = {
        'nombre': request.form['nombre']
    }

    Producto.save(datos)
    flash("Producto ingresado correctamente", "success")
    return redirect("/productos")
# endregion
# region EDITAR
@app.route("/productos/<int:id>/editar")
def producto_actualizar(id):

    objeto = Producto.get(id)
    sujeto = "producto"

    return render_template("productos/formulario_editar.html", sujeto=sujeto, objeto=objeto)


@app.route("/productos/<int:id>/editar", methods=["POST"])
def procesar_editar_productos(id):
    objeto = Producto.get(id)
    objeto.nombre = request.form['nombre']
    objeto.update()

    flash("Producto actualizado correctamente", "success")
    return redirect("/productos")
# endregion


@app.route("/productos/<int:id>/eliminar")
def procesar_eliminado_producto(id):

    Producto.delete(id)
    flash("Producto eliminado correctamente", "success")

    return redirect("/productos")
