from flask import render_template, request, redirect
import csv
from registro_ig import app


@app.route("/")
def index():
    fichero = open("data/movimientos.txt", "r")
    csvReader = csv.reader(fichero, delimiter=',', quotechar='"')
    movimientos = []
    for movimiento in csvReader:
        movimientos.append(movimiento)

    # movimientos = [movimiento for movimiento in csvReader] #list comprehension

    fichero.close()
    return render_template("index.html", pageTitle="Lista", movements=movimientos)

@app.route("/nuevo", methods=["GET", "POST"])
def alta():
    if request.method == "GET":
        return render_template("new.html", pageTitle="Alta")
    else:
        fichero = open("data/movimientos.txt", "a", newline="")
        csvWriter = csv.writer(fichero, delimiter=",", quotechar='"')

        #1ª validar que request.form.date <= hoy 
        #si date > hoy devolver el formulario vacío

        csvWriter.writerow([request.form['date'], request.form['concept'], request.form['quantity']])
        fichero.close()

        return redirect("/")