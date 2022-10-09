from modulosG import TablaModulos
from structsG import TablaStruct
from funcionesG import TablaF
import gramatica as g
from interprete import procesar_instrucciones, procesar_globales
from Errores import *
from ts import *
from tipoDato import *
from ambito import *
from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

tErrores = TablaErrores()
ts = TablaSimbolos()
ts.nombre = "Global"
consola = Impresion()
ambito = AmbitoTS("Unico")
ambito.ingresar(ts)
tf = TablaF()
tstruct = TablaStruct()
tm = TablaModulos()
input1 = ""
data = Datos(consola, tErrores, ambito, tf, tstruct, tm, input1)


@app.route('/interpretar', methods=['POST'])
def interpretar():
    input = request.json['texto']
    global data
    data.ambito.limpiar()
    ts = TablaSimbolos()
    ts.nombre = "Global"
    data.ambito.ingresar(ts)
    data.errores.limpiar()
    data.funciones.limpiar()
    data.structs.limpiar()
    data.modulos.limpiar()
    data.texto = ""
    data.texto = input
    data.consola.cadena = ""
    raiz = g.parse(input)
    
    #para encontrar todas las funciones, structs y modulos globales
    procesar_globales(raiz, data)

    for fn in data.funciones.funciones:
        if fn.nombre == "main":
            procesar_instrucciones(fn.instrucciones, data)
    if len(data.errores.errores) == 0:
        Dato = {
            'message':'Success',
            'consola': data.consola.cadena
            }
        
    else:
        Dato = {
            'message':'Error',
            'consola': "hay errores en el archivo de entrada, ver reporte de errores"
            }
    respuesta = jsonify(Dato)
    print("longitud ambito global......", len(data.ambito.pila[0].simbolos))
    print("longitud tabla errores......",len(data.errores.errores))
    print("tablas de simbolos en ambito",data.ambito.longitud())
    print("funciones globales..........",len(data.funciones.funciones))
    print("structs globales............",len(data.structs.structs))
    print("modulos globales............", len(data.modulos.modulos))
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

@app.route('/structs', methods=['GET'])
def reporte_structs():
    if len(data.structs.structs) == 0:
        Dato = {
            'message':'Vacio',
            'consola': "No hay errores en el archivo"
            }
        
    else:
        data.structs.generarHTML()
        Dato = {
            'message':'Success',
            'consola': "reporte generado con exito"
            }
    respuesta = jsonify(Dato)
    return respuesta

@app.route('/funciones', methods=['GET'])
def reporte_funciones():
    if len(data.funciones.funciones) == 0:
        Dato = {
            'message':'Vacio',
            'consola': "No hay errores en el archivo"
            }
        
    else:
        data.funciones.generarHTML()
        Dato = {
            'message':'Success',
            'consola': "reporte generado con exito"
            }
    respuesta = jsonify(Dato)
    return respuesta

@app.route('/simbolos', methods=['GET'])
def reporte_simbolos():
    if len(data.ambito.pila[0].simbolos) == 0:
        Dato = {
            'message':'Vacio',
            'consola': "No hay errores en el archivo"
            }
        
    else:
        data.ambito.pila[0].generarHTML()
        Dato = {
            'message':'Success',
            'consola': "reporte generado con exito"
            }
    respuesta = jsonify(Dato)
    return respuesta

@app.route('/DB', methods=['GET'])
def reporte_bases():
    if len(data.ambito.pila[0].simbolos) == 0:
        Dato = {
            'message':'Vacio',
            'consola': "No hay errores en el archivo"
            }
    else:
        data.modulos.generarHTML()
        Dato = {
            'message':'Success',
            'consola': "reporte generado con exito"
            }
    respuesta = jsonify(Dato)
    return respuesta

@app.route('/DBT', methods=['GET'])
def reporte_tablas_bases():
    if len(data.ambito.pila[0].simbolos) == 0:
        Dato = {
            'message':'Vacio',
            'consola': "No hay errores en el archivo"
            }
    else:
        data.modulos.generarHTMLTablas()
        Dato = {
            'message':'Success',
            'consola': "reporte generado con exito"
            }
    respuesta = jsonify(Dato)
    return respuesta


#print (len(data.ambito.pila[1].simbolos))
#data.ambito.pila[2].generarHTML()
#data.ambito.pila[0].generarHTML()
#data.errores.generarHTML()

app.run(port=3000, debug=True)