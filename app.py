from flask import Flask, request, redirect, render_template

app = Flask(__name__)
app.jinja_env.globals['enumerate'] = enumerate

tareas = []

def agregar_tarea(tareas, nombre, fecha):
    tarea = {"nombre": nombre, "fecha": fecha, "completada": False}
    tareas.append(tarea)

def completar_tarea(tareas, numero):
    if 1 <= numero <= len(tareas):
        tareas[numero - 1]["completada"] = True

def eliminar_tarea(tareas, numero):
    if 1 <= numero <= len(tareas):
        tareas.pop(numero - 1)

@app.route("/")
def index():
    total = len(tareas)
    completadas = sum(1 for t in tareas if t["completada"])
    pendientes = total - completadas
    return render_template("index.html", tareas=tareas,
                           total=total, completadas=completadas, pendientes=pendientes)

@app.route("/agregar", methods=["POST"])
def agregar():
    nombre = request.form["nombre"]
    fecha = request.form["fecha"]
    if nombre.strip():
        agregar_tarea(tareas, nombre, fecha)
    return redirect("/")

@app.route("/completar/<int:numero>", methods=["POST"])
def completar(numero):
    completar_tarea(tareas, numero)
    return redirect("/")

@app.route("/eliminar/<int:numero>", methods=["POST"])
def eliminar(numero):
    eliminar_tarea(tareas, numero)
    return redirect("/")

if __name__ == "__main__":
    app.run(debug=True)
