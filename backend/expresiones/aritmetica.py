from expresiones.expresiones import *
from tipoDato import Retorno

def aritmetica(r1, r2, op, fila, columna, data):
    tipo1 = r1.tipo
    tipo2 = r2.tipo
    res = Retorno()
    if(r1.valor == "error" or r2.valor == "error"):
        res.valor = "error"
        res.linea = fila
        res.columna = columna
        return res
    if(tipo1 == "CADENA" and tipo2 == "CADENA"):
        res.tipo = "CADENA"
        res.valor =  r1.valor + r2.valor
        res.linea = fila
        res.columna = columna
        return res
    else:
        if(tipo1 == "ENTERO" or tipo1 == "DECIMAL"):
            if(tipo1 == tipo2):
                res.tipo = r1.tipo
                res.linea = fila
                res.columna = columna
                if op == OPERACION_ARITMETICA.MAS: res.valor = r1.valor + r2.valor
                elif op == OPERACION_ARITMETICA.MENOS: res.valor = r1.valor - r2.valor
                elif op == OPERACION_ARITMETICA.POR: res.valor = r1.valor * r2.valor
                elif op == OPERACION_ARITMETICA.DIVIDIDO: 
                    if r2.valor == 0:
                        data.errores.insertar("No es posible la division entre 0", data.ambito.pila[len(data.ambito.pila)-1].nombre, fila, columna, data.texto)
                    else:
                        temp_res = r1.valor / r2.valor
                        if tipo1 == "ENTERO":
                            res.valor = int(temp_res)
                        else:
                            res.valor = temp_res
                elif op == OPERACION_ARITMETICA.MODULO: res.valor = r1.valor % r2.valor
                else:
                    res.valor = "error"
                    data.errores.insertar("No es posible hacer operacion", data.ambito.pila[len(data.ambito.pila)-1].nombre, fila, columna, data.texto)
            else:
                data.errores.insertar("No es posible hacer operacion aritmetica los tipos de datos no son iguales", data.ambito.pila[len(data.ambito.pila)-1].nombre, fila, columna, data.texto)
                res.valor = "error"
                
        else:
            data.errores.insertar("No es posible hacer operacion aritmetica con ID, CHAR, BOOL", data.ambito.pila[len(data.ambito.pila)-1].nombre, fila, columna, data.texto)
            #print("no es posible hacer operacion")
            res.valor = "error"

        return res

def unaria(r1, op, fila, columna, data):
    tipo1 = r1.tipo
    res = Retorno()
    res.linea = fila
    res.columna = columna
    if(r1.valor == "error"):
        res.valor = "error"
        return res
    if op == "!":
        res.tipo = "BOOL"
        res.valor = not r1.valor
    elif op == "-":
        if tipo1 == "ENTERO" or tipo1 == "DECIMAL":
            res.tipo = tipo1
            res.valor = r1.valor * -1
        else:
            data.errores.insertar("no es posible usar este operador en char, string o bool", data.ambito.pila[len(data.ambito.pila)-1].nombre, fila, columna, data.texto)
            res.valor = "error"
    else:
        print("no se que ha pasado")
        res.valor = "error"
    return res

def potencia(r1, r2, tipo, tipoP, fila, columna, data):

    tipo1 = r1.tipo
    tipo2 = r2.tipo
    res = Retorno()
    res.linea = fila
    res.columna = columna
    if(r1.valor == "error" or r2.valor == "error"):
        res.valor = "error"
        return res
    if( tipo1 == tipo2):
        if tipo.value == "i64" and tipo1 == "ENTERO" and tipoP == "::pow":
            res.tipo = tipo1
            res.valor = r1.valor**r2.valor
        elif tipo.value == "f64" and tipo1 == "DECIMAL" and tipoP == "::powf":
            res.tipo = tipo1
            res.valor = r1.valor**r2.valor
        else:
            res.valor = "error"
            data.errores.insertar("no se cumple el formato para la operacion potencia", data.ambito.pila[len(data.ambito.pila)-1].nombre, fila, columna, data.texto)
    else:
        res.valor = "error"
        data.errores.insertar("las expresiones no son iguales, no se puede realizar la operacion", data.ambito.pila[len(data.ambito.pila)-1].nombre, fila, columna, data.texto)
    return res
        