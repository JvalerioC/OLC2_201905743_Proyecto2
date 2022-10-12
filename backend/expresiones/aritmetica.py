from expresiones.expresiones import *
from tipoDato import Retorno, Texp

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
                        data.errores.insertar("No es posible la division entre 0", "", fila, columna, data.texto)
                    else:
                        temp_res = r1.valor / r2.valor
                        if tipo1 == "ENTERO":
                            res.valor = int(temp_res)
                        else:
                            res.valor = temp_res
                elif op == OPERACION_ARITMETICA.MODULO: res.valor = r1.valor % r2.valor
                else:
                    res.valor = "error"
                    data.errores.insertar("No es posible hacer operacion", "", fila, columna, data.texto)
            else:
                data.errores.insertar("No es posible hacer operacion aritmetica los tipos de datos no son iguales", "", fila, columna, data.texto)
                res.valor = "error"
                
        else:
            data.errores.insertar("No es posible hacer operacion aritmetica con ID, CHAR, BOOL", "", fila, columna, data.texto)
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
            data.errores.insertar("no es posible usar este operador en char, string o bool", "", fila, columna, data.texto)
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
            data.errores.insertar("no se cumple el formato para la operacion potencia", "", fila, columna, data.texto)
    else:
        res.valor = "error"
        data.errores.insertar("las expresiones no son iguales, no se puede realizar la operacion", "", fila, columna, data.texto)
    return res
        
def t_unaria(r1, op, fila, columna, data):
    te = Texp("", "", fila, columna)

    if op == "!":
        temporal = data.obtenerTemporal()
        te.direccion = temporal
        te.codigo += r1.codigo
        te.codigo += "\n" + temporal + " = !"+r1.direccion+";"
    elif op == "-":
        temporal = data.obtenerTemporal()
        te.direccion = temporal
        te.codigo += temporal + " = -"+r1.direccion+";"

    return te

def t_potencia(r1, r2, tipo, tipoP, fila, columna, data):

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
            data.errores.insertar("no se cumple el formato para la operacion potencia", "", fila, columna, data.texto)
    else:
        res.valor = "error"
        data.errores.insertar("las expresiones no son iguales, no se puede realizar la operacion", "", fila, columna, data.texto)
    return res

def t_aritmetica(r1, r2, op, fila, columna, data):
    te = Texp("", "", fila, columna)
    tipo1 = r1.tipo
    tipo2 = r2.tipo
    if(tipo1 == "ENTERO" or tipo1 == "DECIMAL"):
        if(tipo1 == tipo2):
            if op == OPERACION_ARITMETICA.MAS: 
                temporal = data.obtenerTemporal()
                t_codigo = "\n"+ temporal +" = "+r1.direccion+" + "+r2.direccion+";"
                te.direccion = temporal
                te.codigo = r1.codigo + r2.codigo + t_codigo
                te.tipo = tipo1
            elif op == OPERACION_ARITMETICA.MENOS: 
                temporal = data.obtenerTemporal()
                t_codigo = "\n"+ temporal +" = "+r1.direccion+" - "+r2.direccion+";"
                te.direccion = temporal
                te.codigo = r1.codigo + r2.codigo + t_codigo
                te.tipo = tipo1
            elif op == OPERACION_ARITMETICA.POR: 
                temporal = data.obtenerTemporal()
                t_codigo = "\n"+ temporal +" = "+r1.direccion+" * "+r2.direccion+";"
                te.direccion = temporal
                te.codigo = r1.codigo + r2.codigo + t_codigo
                te.tipo = tipo1
            elif op == OPERACION_ARITMETICA.DIVIDIDO: 
                etiqueta = data.obtenerEtiqueta()
                te_codigo = "\nif("+r2.direccion+"!= 0) goto "+etiqueta+";"
                te_codigo += "\nprintf(\"%c\", 77);"
                te_codigo += "\nprintf(\"%c\", 97);"
                te_codigo += "\nprintf(\"%c\", 116);"
                te_codigo += "\nprintf(\"%c\", 104);"
                te_codigo += "\nprintf(\"%c\", 69);"
                te_codigo += "\nprintf(\"%c\", 114);"
                te_codigo += "\nprintf(\"%c\", 114);"
                te_codigo += "\nprintf(\"%c\", 111);"
                te_codigo += "\nprintf(\"%c\", 114);"
                temporal = data.obtenerTemporal()
                te.direccion = temporal
                te_codigo += "\n"+temporal+" = 0;"
                te_codigo += "\n goto "+ data.obtenerEtiqueta()
                te_codigo += "\n"+data.obtenerEtiquetaAnterior()+":"
                t_codigo = "\n"+ temporal +" = "+r1.direccion+" / "+r2.direccion+";"
                te.codigo = r1.codigo + r2.codigo + t_codigo
                te_codigo += "\n"+etiqueta+":"
                te.tipo = tipo1
                
            elif op == OPERACION_ARITMETICA.MODULO: 
                etiqueta = data.obtenerEtiqueta()
                te_codigo = "\nif("+r2.direccion+"!= 0) goto "+etiqueta+";"
                te_codigo += "\nprintf(\"%c\", 77);"
                te_codigo += "\nprintf(\"%c\", 97);"
                te_codigo += "\nprintf(\"%c\", 116);"
                te_codigo += "\nprintf(\"%c\", 104);"
                te_codigo += "\nprintf(\"%c\", 69);"
                te_codigo += "\nprintf(\"%c\", 114);"
                te_codigo += "\nprintf(\"%c\", 114);"
                te_codigo += "\nprintf(\"%c\", 111);"
                te_codigo += "\nprintf(\"%c\", 114);"
                temporal = data.obtenerTemporal()
                te.direccion = temporal
                te_codigo += "\n"+temporal+" = 0;"
                te_codigo += "\n goto "+ data.obtenerEtiqueta()
                te_codigo += "\n"+data.obtenerEtiquetaAnterior()+":"
                t_codigo = "\n"+ temporal +" = "+r1.direccion+" % "+r2.direccion+";"
                te.codigo = r1.codigo + r2.codigo + t_codigo
                te_codigo += "\n"+etiqueta+":"
                te.tipo = tipo1
            else:
                te = "error"
                print("2")
                data.errores.insertar("No es posible hacer operacion", "", fila, columna, data.texto)
        else:
            data.errores.insertar("No es posible hacer operacion aritmetica los tipos de datos no son iguales", "", fila, columna, data.texto)
            te = "error"
            print("3")
    else:
        print("1")
        data.errores.insertar("No es posible hacer operacion aritmetica con ID, CHAR, BOOL", "", fila, columna, data.texto)
        #print("no es posible hacer operacion")
        te = "error"

    return te