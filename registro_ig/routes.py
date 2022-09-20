from flask import render_template, request, redirect
import csv
from registro_ig import app
from datetime import date


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
        return render_template("new.html", pageTitle="Alta", 
                               dataForm={})
    else:
        """
            1. Validar el formulario
                Fecha valida y <= hoy
            2. Concepto no sea vacío
            3. Cantidad no se cero     
        """
        errores = validaFormulario(request.form)

        if not errores:
            fichero = open("data/movimientos.txt", "a", newline="")
            csvWriter = csv.writer(fichero, delimiter=",", quotechar='"')

            csvWriter.writerow([request.form['date'], request.form['concept'], request.form['quantity']])
            fichero.close()

            return redirect("/")
        else:
            return render_template("new.html", pageTitle="Alta", msgErrors=errores, dataForm=dict(request.form))

def validaFormulario(camposFormulario):
    errores = []
    hoy = date.today().isoformat()
    if camposFormulario['date'] > hoy:
        errores.append("La fecha introducida es es futuro.")

    if camposFormulario['concept'] == "":
        errores.append("Introduce un concepto para la transacción.")

    #La primera condición es para que el número sea distinto de cero
    #la segunda condición es para que el campo no esté vacío
    if camposFormulario["quantity"] == "" or float(camposFormulario["quantity"]) == 0.0:
        errores.append("Introduce una cantidad positiva o negativa.")

    return errores

    
