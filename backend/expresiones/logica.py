from expresiones.expresiones import *
from tipoDato import Retorno

def logica(r1, r2, op, fila, columna, data):
    tipo1 = r1.tipo
    tipo2 = r2.tipo
    res = Retorno()
    if(r1.valor == "error" or r2.valor == "error"):
        res.valor = "error"
        res.tipo = r1.tipo
        res.linea = fila
        res.columna = columna
        return res
    if(tipo1 == tipo2 and tipo1 == "BOOL"):
        res.tipo = tipo1
        res.linea = fila
        res.columna = columna
        if op == OPERACION_LOGICA.AND: res.valor = r1.valor and r2.valor
        elif op == OPERACION_LOGICA.OR: res.valor = r1.valor or r2.valor
        else:
            res.valor = "error"
            data.errores.insertar("No es posible hacer operacion", data.ambito.pila[len(data.ambito.pila)-1].nombre, fila, columna, data.texto)
    else:
        data.errores.insertar("No es posible hacer operacion logica los tipos de datos no son iguales o no son booleanos", data.ambito.pila[len(data.ambito.pila)-1].nombre, fila, columna, data.texto)
        res.valor = "error"
    return res