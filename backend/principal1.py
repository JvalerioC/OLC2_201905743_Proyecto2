import gramatica as g
from interprete import procesar_globales, procesar_instrucciones
from Errores import *
from ts import *
from tipoDato import *

tErrores = TablaErrores()
ts = TablaSimbolos()
consola = Impresion()

f = open("./entrada.txt", "r", encoding="utf-8")
input = f.read()
f.close()
#print(input)
raiz = g.parse(input)

data = Datos(consola, tErrores, ts, input)
#para encontrar todas las funciones, structs y modulos globales
procesar_globales(raiz, data)

data.pStack = 0
data.pHeap = 0
#aqui tengo que poner lo de la creacion de la funcion en C3D
procesar_instrucciones(raiz, data)

print("longitud ambito global......", len(data.ts.simbolos))
print("longitud tabla errores......", len(data.errores.errores))
data.encabezado += data.generar_etiquetas()
data.encabezado += data.consola.cadena
print(data.encabezado)

#print (len(data.ambito.pila[1].simbolos))
#data.ts.generarHTML() #para ver la tabla de simbolos
#data.errores.generarHTML()