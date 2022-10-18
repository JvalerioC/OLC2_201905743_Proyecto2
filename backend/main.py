import gramatica as g
from interprete import procesar_globales, procesar_instrucciones
from Errores import *
from ts import *
from tipoDato import *
from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

tErrores = TablaErrores()
ts = TablaSimbolos()
consola = Impresion()
input1 = ""

data = Datos(consola, tErrores, ts, input1)
#d1*d2*z+j*d1+i para arreglos y vectores

@app.route('/interpretar', methods=['POST'])
def interpretar():
    input = request.json['texto']
    global data
    data.errores.limpiar()
    ts1 = TablaSimbolos()
    data.ts = ts1
    data.texto = ""
    data.texto = input
    data.consola.cadena = ""
    data.encabezado = "#include <stdio.h>\n"
    data.encabezado += "float stack[100000]; // Stack\n"
    data.encabezado += "float heap[100000]; // Heap\n"
    data.encabezado += "float P; // Puntero Stack\n"
    data.encabezado += "float H; // Puntero Heap\n"
    data.temporal = 0
    data.etiqueta = 0
    raiz = g.parse(input)
    #para encontrar todas las funciones, structs y modulos globales
    procesar_globales(raiz, data)
    data.pHeap = 0
    data.pStack = 0

    procesar_instrucciones(raiz, data)
    if len(data.errores.errores) == 0:
        data.encabezado += data.generar_etiquetas()
        data.encabezado += data.consola.cadena
        Dato = {
            'message':'Success',
            'consola': data.encabezado
            }
        
    else:
        Dato = {
            'message':'Error',
            'consola': "hay errores en el archivo de entrada, ver reporte de errores"
            }
    respuesta = jsonify(Dato)
    print("longitud ambito global......", len(data.ts.simbolos))
    print("longitud tabla errores......", len(data.errores.errores))
    return(respuesta)

@app.route('/errores', methods=['GET'])
def reporte_errores():
    if len(data.errores.errores) == 0:
        Dato = {
            'message':'Vacio',
            'consola': "No hay errores en el archivo"
            }
        
    else:
        data.errores.generarHTML()
        Dato = {
            'message':'Success',
            'consola': "reporte generado con exito"
            }
    respuesta = jsonify(Dato)
    return respuesta

@app.route('/simbolos', methods=['GET'])
def reporte_simbolos():
    if len(data.ts.simbolos) == 0:
        Dato = {
            'message':'Vacio',
            'consola': "No hay errores en el archivo"
            }
        
    else:
        data.ts.generarHTML()
        Dato = {
            'message':'Success',
            'consola': "reporte generado con exito"
            }
    respuesta = jsonify(Dato)
    return respuesta


app.run(port=3000, debug=True)