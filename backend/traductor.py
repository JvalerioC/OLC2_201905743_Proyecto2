from expresiones.operacion import *

def procesar_imprimir(inst, data):
    op = Operacion()
    dato = op.ejecutar(inst, data)

    if dato.tipo == "CADENA":
        for caracter in dato.valor:
            ascii_char = str(ord(caracter))
            data.consola.concatenar(f"printf(\"%c\", {ascii_char}); ")
            data.consola.concatenar("\n")
        data.consola.concatenar("printf(\"%c\", 10); ")
        data.consola.concatenar("\n")
    else:
        temp_ambito = data.ts.nombre_entorno()
        data.errores.insertar("la expresion a imprimir no es de tipo cadena", temp_ambito, dato.linea, dato.columna, data.texto)
    
def procesar_imprimire(cadena, expresiones, data):
    print("soy una impresion de una expresion")

def procesar_declaracion1(id, expresion, data):
    print("soy una declaracion sin tipo")