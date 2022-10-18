from expresiones.expresiones import *
from tipoDato import Retorno, Texp

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
            data.errores.insertar("No es posible hacer operacion", "", fila, columna, data.texto)
    else:
        data.errores.insertar("No es posible hacer operacion relacional los tipos de datos no son iguales", "", fila, columna, data.texto)
        #print("no es posible")
        res.valor = "error"
    return res

def t_relacional(r1, r2, op, fila, columna, data):
    tipo1 = r1.tipo
    tipo2 = r2.tipo
    te = Texp("", "", fila, columna)
    if(r1 == "error" or r2 == "error"):
        te = "error"
        return te
    if(tipo1 == tipo2):
        #print(op, r1.valor, r2.valor)
        te.tipo = "BOOL"
        te.linea = fila
        te.columna = columna
        if op == OPERACION_RELACIONAL.IGUAL:
            tempV = data.obtenerEtiqueta()
            tempF = data.obtenerEtiqueta() 
            t_codigo = "\n"
            t_codigo += "if ("+r1.direccion+" == "+r2.direccion+") goto "+tempV+";"
            t_codigo += "\n" 
            t_codigo += "goto "+tempF+";"
            te.etiquetaF = tempF
            te.etiquetaV = tempV
            te.tipo = "BOOL"
            te.codigo = r1.codigo+r2.codigo+t_codigo
        elif op == OPERACION_RELACIONAL.DIFERENTE: 
            tempV = data.obtenerEtiqueta()
            tempF = data.obtenerEtiqueta() 
            t_codigo = "\n"
            t_codigo += "if ("+r1.direccion+" != "+r2.direccion+") goto "+tempV+";"
            t_codigo += "\n" 
            t_codigo += "goto "+tempF+";"
            te.etiquetaF = tempF
            te.etiquetaV = tempV
            te.tipo = "BOOL"
            te.codigo = r1.codigo+r2.codigo+t_codigo
        elif op == OPERACION_RELACIONAL.MAYOR_QUE: 
            tempV = data.obtenerEtiqueta()
            tempF = data.obtenerEtiqueta() 
            t_codigo = "\n"
            t_codigo += "if ("+r1.direccion+" > "+r2.direccion+") goto "+tempV+";"
            t_codigo += "\n" 
            t_codigo += "goto "+tempF+";"
            te.etiquetaF = tempF
            te.etiquetaV = tempV
            te.tipo = "BOOL"
            te.codigo = r1.codigo+r2.codigo+t_codigo
        elif op == OPERACION_RELACIONAL.MAYOR_IGUAL: 
            tempV = data.obtenerEtiqueta()
            tempF = data.obtenerEtiqueta() 
            t_codigo = "\n"
            t_codigo += "if ("+r1.direccion+" >= "+r2.direccion+") goto "+tempV+";"
            t_codigo += "\n" 
            t_codigo += "goto "+tempF+";"
            te.etiquetaF = tempF
            te.etiquetaV = tempV
            te.tipo = "BOOL"
            te.codigo = r1.codigo+r2.codigo+t_codigo
        elif op == OPERACION_RELACIONAL.MENOR_QUE:
            tempV = data.obtenerEtiqueta()
            tempF = data.obtenerEtiqueta() 
            t_codigo = "\n"
            t_codigo += "if ("+r1.direccion+" < "+r2.direccion+") goto "+tempV+";"
            t_codigo += "\n" 
            t_codigo += "goto "+tempF+";"
            te.etiquetaF = tempF
            te.etiquetaV = tempV
            te.tipo = "BOOL"
            te.codigo = r1.codigo+r2.codigo+t_codigo
        elif op == OPERACION_RELACIONAL.MENOR_IGUAL: 
            tempV = data.obtenerEtiqueta()
            tempF = data.obtenerEtiqueta() 
            t_codigo = "\n"
            t_codigo += "if ("+r1.direccion+" <= "+r2.direccion+") goto "+tempV+";"
            t_codigo += "\n" 
            t_codigo += "goto "+tempF+";"
            te.etiquetaF = tempF
            te.etiquetaV = tempV
            te.tipo = "BOOL"
            te.codigo = r1.codigo+r2.codigo+t_codigo
        else:
            te.valor = "error"
            data.errores.insertar("No es posible hacer operacion", "", fila, columna, data.texto)
    else:
        data.errores.insertar("No es posible hacer operacion relacional los tipos de datos no son iguales", "", fila, columna, data.texto)
        #print("no es posible")
        te.valor = "error"
    return te