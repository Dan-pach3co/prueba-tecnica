from flask import Flask, render_template, request, redirect, url_for, flash
app = Flask(__name__)
app.secret_key = "RaeAlert" 

#lista diccionario predeterminada 
tasks = [
    {"id": 1, 
     "titulo": "Investigacion derechos humanos", 
     "estado": "en_progreso", 
     "fecha": "2025-11-25"},

    {"id": 2, 
     "titulo": "Mapa mental sobre variables aleatorias", 
     "estado": "completada", 
     "fecha": "2025-11-20"},

    {"id": 3, 
     "titulo": "Dashboard de productos", 
     "estado": "pendiente", 
     "fecha": "2025-11-30"},
]
next_id = 4

@app.route("/")
def task_list():
    filtro = request.args.get('estado')
    if filtro and filtro != 'todas':
        tareas_filtradas = [t for t in tasks if t["estado"] == filtro] #filtra por estado seleccionado si no son todos
    else:
        tareas_filtradas = tasks
    return render_template("index.html", tasks=tareas_filtradas)


@app.route("/add", methods=["POST"])
def add_task():
    global next_id
    titulo = request.form.get("titulo")
    fecha = request.form.get("fecha")
    
    if titulo:
        nueva_tarea = {
            "id": next_id,
            "titulo": titulo,
            "estado": "pendiente", 
            "fecha": fecha
        }
        tasks.append(nueva_tarea)
        next_id += 1
        flash("¡Tarea creada exitosamente!", "success")
    return redirect("/")


@app.route("/delete/<int:task_id>")
def delete_task(task_id):
    global tasks
    tasks = [task for task in tasks if task["id"] != task_id] #reescribe la lista
    flash("Tarea eliminada correctamente.", "danger")
    return redirect("/")


@app.route("/edit/<int:task_id>", methods=["GET", "POST"])
def edit_task(task_id):
    
    tarea_a_editar = next((t for t in tasks if t["id"] == task_id), None) #busca la tarea
    
    if not tarea_a_editar:
        return redirect("/")

    if request.method == "POST":
        tarea_a_editar['titulo'] = request.form.get('titulo')
        tarea_a_editar['fecha'] = request.form.get('fecha')
        tarea_a_editar['estado'] = request.form.get('estado')
        return redirect("/") 
    return render_template("index.html", tasks=tasks, task_to_edit=tarea_a_editar)


@app.route("/detail/<int:task_id>")
def view_detail(task_id):
    tarea = next((t for t in tasks if t["id"] == task_id), None)
    
    # Si no existe la tarea vuelve al inicio normal
    if not tarea:
        return redirect("/")
    return render_template("index.html", detail=tarea, tasks=tasks)

if __name__ == "__main__":
    app.run(debug=True)


