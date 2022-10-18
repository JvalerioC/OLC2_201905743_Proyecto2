from expresiones.expresiones import *
from tipoDato import Retorno, Texp

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

def t_logica(r1, r2, op, fila, columna, data):
    te = Texp("", "", fila, columna)
    if(r1 == "error" or r2 == "error"):
        te = "error"
        return te
    tipo1 = r1.tipo
    tipo2 = r2.tipo
    if(tipo1 == tipo2 and tipo1 == "BOOL"):
        if r1.etiquetaV == None:
            tempV = data.obtenerEtiqueta()
            tempF = data.obtenerEtiqueta() 
            t_codigo = "\n"
            t_codigo += "if ("+r1.direccion+" == 1) goto "+tempV+";"
            t_codigo += "\n" 
            t_codigo += "goto "+tempF+";"
            r1.etiquetaF = tempF
            r1.etiquetaV = tempV
            te.codigo = t_codigo

        if r2.etiquetaV == None:
            tempV = data.obtenerEtiqueta()
            tempF = data.obtenerEtiqueta() 
            t_codigo = "\n"
            t_codigo += "if ("+r1.direccion+" == 1) goto "+tempV+";"
            t_codigo += "\n" 
            t_codigo += "goto "+tempF+";"
            r2.etiquetaF = tempF
            r2.etiquetaV = tempV
            te.codigo = t_codigo
            
        te.tipo = tipo1
        te.linea = fila
        te.columna = columna
        if op == OPERACION_LOGICA.AND:
            tempF = r1.etiquetaF + ","+ r2.etiquetaF
            tempV = r2.etiquetaV
            te.etiquetaF = tempF
            te.etiquetaV =  tempV
            te.codigo = r1.codigo +"\n"+r1.obtenerV()+"\n"+r2.codigo
        elif op == OPERACION_LOGICA.OR: 
            tempV = r1.etiquetaV + ","+ r2.etiquetaV
            tempF = r2.etiquetaF
            te.etiquetaF = tempF
            te.etiquetaV =  tempV
            te.codigo = r1.codigo +"\n"+r1.obtenerF()+"\n"+r2.codigo
        else:
            te = "error"
            data.errores.insertar("No es posible hacer operacion", "", fila, columna, data.texto)
    else:
        data.errores.insertar("No es posible hacer operacion logica los tipos de datos no son iguales o no son booleanos", "", fila, columna, data.texto)
        te = "error"
    return te