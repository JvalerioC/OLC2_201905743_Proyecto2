from expresiones.expresiones import *
from tipoDato import Retorno

def relacional(r1, r2, op, fila, columna, data):
    tipo1 = r1.tipo
    tipo2 = r2.tipo
    res = Retorno()
    if(r1.valor == "error" or r2.valor == "error"):
        res.valor = "error"
        res.tipo = r1.tipo
        res.linea = fila
        res.columna = columna
        return res
    if(tipo1 == tipo2):
        #print(op, r1.valor, r2.valor)
        res.tipo = "BOOL"
        res.linea = fila
        res.columna = columna
        if op == OPERACION_RELACIONAL.IGUAL: res.valor = r1.valor == r2.valor
        elif op == OPERACION_RELACIONAL.DIFERENTE: res.valor = r1.valor != r2.valor
        elif op == OPERACION_RELACIONAL.MAYOR_QUE: res.valor = r1.valor > r2.valor
        elif op == OPERACION_RELACIONAL.MAYOR_IGUAL: res.valor = r1.valor >= r2.valor
        elif op == OPERACION_RELACIONAL.MENOR_QUE: res.valor = r1.valor < r2.valor
        elif op == OPERACION_RELACIONAL.MENOR_IGUAL: res.valor = r1.valor <= r2.valor
        else:
            res.valor = "error"
            data.errores.insertar("No es posible hacer operacion", data.ambito.pila[len(data.ambito.pila)-1].nombre, fila, columna, data.texto)
    else:
        data.errores.insertar("No es posible hacer operacion relacional los tipos de datos no son iguales", data.ambito.pila[len(data.ambito.pila)-1].nombre, fila, columna, data.texto)
        #print("no es posible")
        res.valor = "error"
    return res