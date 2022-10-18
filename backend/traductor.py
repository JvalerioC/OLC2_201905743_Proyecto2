from expresiones.operacion import *
from expresiones.eTraduccion import *

def procesar_imprimir(inst, data):
    op = Operacion()
    dato = op.ejecutar(inst, data)

    if dato.tipo == "CADENA":
        data.consola.concatenar("\n")
        for caracter in dato.valor:
            ascii_char = str(ord(caracter))
            data.consola.concatenar(f"printf(\"%c\", {ascii_char}); ")
            data.consola.concatenar("\n")
        data.consola.concatenar("printf(\"%c\", 10); ")
    else:
        temp_ambito = data.ts.nombre_entorno()
        data.errores.insertar("la expresion a imprimir no es de tipo cadena", temp_ambito, dato.linea, dato.columna, data.texto)
    
def procesar_imprimire(cadena, expresiones, data):
    op = Operacion()
    dato = op.ejecutar(cadena, data)
    if dato.tipo == "CADENA":
        if "{:?}" in dato.valor:
            procesar_imprimirV(cadena, expresiones[0], data)
        else:
            temp = dato.valor.split("{}")
            if len(temp)-1 == len(expresiones):
                cadena_temp = "\n"
                tipo_impresion = ""
                casteo = ""
                hubo_error = False
                for i in range(len(expresiones)):
                    cadena_temp += "\n"
                    for caracter in temp[i]:
                        ascii_char = str(ord(caracter))
                        cadena_temp += "\n"
                        cadena_temp += f"printf(\"%c\", {ascii_char}); "

                    exp_temp = op.ejecutar(expresiones[i], data)
                    #print(exp_temp.tipo)
                    if(exp_temp.valor == "error"):
                        hubo_error = True
                        break
                    elif exp_temp.tipo == "ENTERO":
                        tipo_impresion = "d"
                        casteo = "(int)"
                    elif exp_temp.tipo == "DECIMAL":
                        tipo_impresion = "f"
                    elif exp_temp.tipo == "CARACTER":
                        tipo_impresion = "c"
                        casteo = "(int)"
                    elif exp_temp.tipo == "CADENA":
                        tipo_impresion = "c"
                        casteo = "(int)"
                    elif exp_temp.tipo == "BOOL":
                        tipo_impresion = "d"
                        casteo = "(int)"

                    if exp_temp.tipo == "CADENA":
                        cadena_temp += "\n"
                        tr = TraductorExp()
                        traduccion = tr.traducir_expresion(expresiones[i], data)
                        cadena_temp += traduccion.codigo
                        cadena_temp += "\n"
                        
                        etiqueta1 = data.obtenerEtiqueta()
                        etiqueta2 = data.obtenerEtiqueta()

                        temporal1 = traduccion.direccion
                        temporal2 = data.obtenerTemporal()
                        temporal3 = data.obtenerTemporal()
                        cadena_temp += temporal2+" = "
                        cadena_temp += f"heap[(int){temporal1}];"
                        cadena_temp += "\n"
                        cadena_temp += temporal3+" = 0;"
                        cadena_temp += "\n"
                        cadena_temp += temporal1+" = "+temporal1+" + 1;"
                        cadena_temp += "\n"
                        cadena_temp += temporal2+" = "+temporal2+" + "+temporal1+";"
                        cadena_temp += "\n"
                        cadena_temp += temporal3+" = "+temporal3+" + "+temporal1+";"
                        cadena_temp += "\n"

                        #aqui va el if
                        cadena_temp += etiqueta1+":\n"
                        cadena_temp += "if("+temporal2+"=="+temporal3+") goto "+etiqueta2+";\n"
                        cadena_temp += temporal1+" = heap[(int)"+temporal3+"];\n"
                        cadena_temp += f"printf(\"%{tipo_impresion}\", {casteo}{temporal1}); "
                        cadena_temp += "\n"
                        cadena_temp += temporal3+" = "+temporal3+" + 1;\n"
                        cadena_temp += "goto "+etiqueta1+";\n"
                        cadena_temp += etiqueta2+":"

                    else:
                        tr = TraductorExp()
                        traduccion = tr.traducir_expresion(expresiones[i], data)
                        cadena_temp += "\n"
                        cadena_temp += traduccion.codigo
                        cadena_temp += "\n"
                        cadena_temp += f"printf(\"%{tipo_impresion}\", {casteo}{traduccion.direccion}); "
                
                for i in temp[len(temp)-1]:
                    ascii_char = str(ord(i))
                    
                    cadena_temp += "\n"
                    cadena_temp += f"printf(\"%c\", {ascii_char}); "
                cadena_temp += "\n"
                cadena_temp += "printf(\"%c\", 10);"

                if hubo_error:
                    data.errores.insertar("la expresion a mostrar no es valida", "", dato.linea, dato.columna, data.texto)
                else:
                    data.consola.concatenar(cadena_temp)
            else:
                data.errores.insertar("la cantidad de expresiones no es valida para imprimir en cadena", "", dato.linea, dato.columna, data.texto)
    else:
        data.errores.insertar("la expresion a imprimir no es de tipo cadena", "", dato.linea, dato.columna, data.texto)
    
def procesar_imprimirV(cadena, expresion, data):
    print()

def procesar_declaracion1(id, expresion, data):
    op = Operacion()
    dato = op.ejecutar(expresion, data)
    if dato.tipo == "CADENA":
        puntero = data.ts.obtener_puntero_stack(id.value, data.pStack, data.pHeap)
        temporal = data.obtenerTemporal()
        data.consola.concatenar("\n")
        data.consola.concatenar(temporal+ " = H;")
        data.consola.concatenar("\n")
        data.consola.concatenar("stack["+str(puntero)+"] = "+temporal+";")
        tr = TraductorExp()
        tr.traducir_expresion(expresion, data)
    else:
        #aqui traduzco la expresion
        tr = TraductorExp()
        traduccion = tr.traducir_expresion(expresion, data)
        if traduccion == "error":
            return
        data.consola.concatenar(traduccion.codigo)
        if traduccion.direccion[0] != "t":
            temporal = data.obtenerTemporal()
            data.consola.concatenar("\n")
            data.consola.concatenar(temporal+" = "+traduccion.direccion+";")
            traduccion.direccion = temporal
        
        puntero = data.ts.obtener_puntero_stack(id.value, data.pStack, data.pHeap)
        temporal = data.obtenerTemporal()
        data.consola.concatenar("\n")
        data.consola.concatenar(temporal+ " = P + "+str(puntero)+";")
        data.consola.concatenar("\n")
        data.consola.concatenar("stack[(int)"+temporal+"] = "+traduccion.direccion+";")

def procesar_declaracion2(id, tipo, expresion, data):
    
    op = Operacion()
    dato = op.ejecutar(expresion, data)
    if dato.tipo == tipoDato(tipo.value):
        if dato.tipo == "CADENA":
            puntero = data.ts.obtener_puntero_stack(id.value, data.pStack, data.pHeap)
            temporal = data.obtenerTemporal()
            data.consola.concatenar("\n")
            data.consola.concatenar(temporal+ " = H;")
            data.consola.concatenar("\n")
            data.consola.concatenar("stack["+str(puntero)+"] = "+temporal+";")
            tr = TraductorExp()
            tr.traducir_expresion(expresion, data)
        else:
            #aqui traduzco la expresion
            tr = TraductorExp()
            traduccion = tr.traducir_expresion(expresion, data)
            if traduccion == "error":
                return
            data.consola.concatenar(traduccion.codigo)
            if traduccion.direccion == "":
                temporal2 = data.obtenerTemporal()
                etiqueta = data.obtenerEtiqueta()
                
                etiquetaV = data.obtenerEtiqueta()
                etiquetaF = data.obtenerEtiqueta()

                cadena_temp = "\n"
                cadena_temp += traduccion.obtenerV()
                cadena_temp += "\n"
                cadena_temp += temporal2+" = 1;"
                cadena_temp += "\n"
                cadena_temp += "goto "+etiqueta+";"
                cadena_temp += "\n"
                cadena_temp += traduccion.obtenerF()
                cadena_temp += "\n"
                cadena_temp += temporal2+" = 0;"
                cadena_temp += "\n"
                cadena_temp += etiqueta+":\n"
                data.consola.concatenar(cadena_temp)
                traduccion.direccion = temporal2

            elif traduccion.direccion[0] != "t":
                temporal = data.obtenerTemporal()
                data.consola.concatenar("\n")
                data.consola.concatenar(temporal+" = "+traduccion.direccion+";")
                traduccion.direccion = temporal
            
            puntero = data.ts.obtener_puntero_stack(id.value, data.pStack, data.pHeap)
            temporal = data.obtenerTemporal()
            data.consola.concatenar("\n")
            data.consola.concatenar(temporal+ " = P + "+str(puntero)+";")
            data.consola.concatenar("\n")
            data.consola.concatenar("stack[(int)"+temporal+"] = "+traduccion.direccion+";")

    else:
        temp_ambito = ""
        data.errores.insertar("el tipo de dato de la variable no coincide con el tipo de la expresion", temp_ambito, id.lineno, id.lexpos, data.texto)

def procesar_if(condicion, instrucciones, data, etiquetaFinal):
    op = Operacion()
    dato =  op.ejecutar(condicion, data)
    if dato.tipo == "BOOL":

        tr = TraductorExp()
        traduccion = tr.traducir_expresion(condicion, data)
        if traduccion == "error":
            return
        etiquetaR = data.obtenerEtiqueta()
        etiquetaV = data.obtenerEtiqueta()
        temporal = data.obtenerTemporal()

        data.consola.concatenar(traduccion.codigo)
        cadena_temp = "\n"
        cadena_temp += traduccion.obtenerV()
        cadena_temp += "\n"
        cadena_temp += temporal+" = 1;"
        cadena_temp += "\n"
        cadena_temp += "goto "+etiquetaR+";"
        cadena_temp += "\n"
        cadena_temp += traduccion.obtenerF()
        cadena_temp += "\n"
        cadena_temp += temporal+" = 0;"
        cadena_temp += "\n"
        cadena_temp += etiquetaR+":\n"
        cadena_temp += "\n"
        if etiquetaFinal == None:
            etiquetaS = data.obtenerEtiqueta()
        else:
            etiquetaS = etiquetaFinal
        cadena_temp += "if("+temporal+" == 1) goto "+etiquetaV+";"
        cadena_temp += "\n"
        cadena_temp += "goto "+etiquetaS+";"
        cadena_temp += "\n"
        cadena_temp += etiquetaV+":"
        cadena_temp += "\n"
        data.consola.concatenar(cadena_temp)

        from interprete import procesar_instrucciones
        procesar_instrucciones(instrucciones, data)
        if etiquetaFinal == None:
            cadena_temp = "\n"
            cadena_temp += etiquetaS+":"
            cadena_temp += "\n"
            data.consola.concatenar(cadena_temp)

    else:
        data.errores.insertar("El valor a evaluar no es booleano", "", dato.linea, dato.columna, data.texto)

def procesar_if_else(condicion, instrucciones, ielse, data, etiquetaFinal):
    op = Operacion()
    dato =  op.ejecutar(condicion, data)
    if dato.tipo == "BOOL":
        tr = TraductorExp()
        traduccion = tr.traducir_expresion(condicion, data)
        if traduccion == "error":
            return
        etiquetaR = data.obtenerEtiqueta()
        etiquetaV = data.obtenerEtiqueta()
        etiquetaF = data.obtenerEtiqueta()
        temporal = data.obtenerTemporal()
        if etiquetaFinal == None:
            etiquetaS = data.obtenerEtiqueta()
        else:
            etiquetaS = etiquetaFinal

        data.consola.concatenar(traduccion.codigo)

        cadena_temp = "\n"
        cadena_temp += traduccion.obtenerV()
        cadena_temp += "\n"
        cadena_temp += temporal+" = 1;"
        cadena_temp += "\n"
        cadena_temp += "goto "+etiquetaR+";"
        cadena_temp += "\n"
        cadena_temp += traduccion.obtenerF()
        cadena_temp += "\n"
        cadena_temp += temporal+" = 0;"
        cadena_temp += "\n"
        cadena_temp += etiquetaR+":\n"
        cadena_temp += "\n"
        cadena_temp += "if("+temporal+" == 1) goto "+etiquetaV+";"
        cadena_temp += "\n"
        cadena_temp += "goto "+etiquetaF+";"
        cadena_temp += "\n"
        cadena_temp += etiquetaV+":"
        cadena_temp += "\n"
        data.consola.concatenar(cadena_temp)
        from interprete import procesar_instrucciones
        procesar_instrucciones(instrucciones, data)
        cadena_temp = "\n"
        cadena_temp += "goto "+etiquetaS+";"
        cadena_temp += "\n"
        cadena_temp += etiquetaF+":"
        cadena_temp += "\n"
        data.consola.concatenar(cadena_temp)

        from instrucciones.instrucciones import If_Else
        from instrucciones.instrucciones import If
        if isinstance(ielse, If_Else) : procesar_if_else(ielse.condicion, ielse.instrucciones, ielse.ielse, data, etiquetaS)
        elif isinstance(ielse, If) : procesar_if(ielse.condicion, ielse.instrucciones, data, etiquetaS)
        else:
            from interprete import procesar_instrucciones
            
            procesar_instrucciones(ielse, data)
        if etiquetaFinal == None:
            data.consola.concatenar("\n"+etiquetaS+":")

def procesar_asignacion(id, expresion, data):
    op = Operacion()
    if  id.type == "ID":
        simbol = data.ts.obtener(id.value, data.pStack, data.pHeap)
        if(simbol == 0):
            data.errores.insertar("La variable no existe", "", id.lineno, id.lexpos, data.texto)
        else:
            if simbol.mutable == True:
                dato = op.ejecutar(expresion, data)
                if(dato.tipo == simbol.tipoDato):
                    if dato.tipo == "CADENA":
                        print()
                    else:
                        puntero = simbol.posicionStack
                        tr = TraductorExp()
                        traduccion = tr.traducir_expresion(expresion, data)
                        data.consola.concatenar("\n")
                        data.consola.concatenar(traduccion.codigo)
                        if traduccion.direccion[0] != "t":
                            temporal = data.obtenerTemporal()
                            data.consola.concatenar("\n")
                            data.consola.concatenar(temporal+" = "+traduccion.direccion+";")
                            traduccion.direccion = temporal
                        
                        temporal = data.obtenerTemporal()
                        data.consola.concatenar("\n")
                        data.consola.concatenar(temporal+ " = P + "+str(puntero)+";")
                        data.consola.concatenar("\n")
                        data.consola.concatenar("stack[(int)"+temporal+"] = "+traduccion.direccion+";")
                        

                    '''if dato.capacidad != None:
                        simbol.capacidad = dato.capacidad
                    simbol.valor = dato.valor
                    data.ambito.modificarSimbolo(simbol, data.ambito.longitud()-1)'''
                else:
                    data.errores.insertar("El tipo de la variable no coincide con el tipo de la expresion a asignar", "", id.lineno, id.lexpos, data.texto)
            else:
                data.errores.insertar("la variable no se puede modificar, no es mutable", "", id.lineno, id.lexpos, data.texto)

def procesar_while(condicion, instrucciones, data):
    op = Operacion()
    dato = op.ejecutar(condicion, data)
    if  dato == "error":
        data.errores.insertar("la expresion no cumple para el ciclo while", "", dato.linea, dato.columna, data.texto)
    else:
        tr = TraductorExp()
        data.isWhile = True
        traduccion = tr.traducir_expresion(condicion, data)
        etiquetaC = data.obtenerEtiqueta()
        etiquetaF = data.obtenerEtiqueta()
        etiquetaV = data.obtenerEtiqueta()
        etiquetaR = data.obtenerEtiqueta()
        temporal = data.obtenerTemporal()
        data.etiquetaSalidaCiclo = etiquetaF
        data.etiquetaRegresoCiclo = etiquetaC
        cadena_temp = "\n"+etiquetaC+":"
        cadena_temp += traduccion.codigo
        cadena_temp += "\n"
        cadena_temp += traduccion.obtenerV()
        cadena_temp += "\n"
        cadena_temp += temporal+" = 1;"
        cadena_temp += "\n"
        cadena_temp += "goto "+etiquetaR+";"
        cadena_temp += "\n"
        cadena_temp += traduccion.obtenerF()
        cadena_temp += "\n"
        cadena_temp += temporal+" = 0;"
        cadena_temp += "\n"+etiquetaR+": "
        cadena_temp += "\nif("+temporal+" == 1) goto "+etiquetaV+";"
        cadena_temp += "\n"
        cadena_temp += "goto "+etiquetaF+";"
        cadena_temp += "\n"
        cadena_temp += etiquetaV+":"
        cadena_temp += "\n"
        data.consola.concatenar(cadena_temp)

        from interprete import procesar_instrucciones
        procesar_instrucciones(instrucciones, data)
        cadena_temp = "\n"
        cadena_temp += "goto "+etiquetaC+";\n"
        cadena_temp += etiquetaF+":"
        data.consola.concatenar(cadena_temp)
        data.isWhile = False
        data.etiquetaSalidaCiclo = None
        data.etiquetaRegresoCiclo = None

def procesar_break(expresion, data):
    if expresion == None:
        if data.isWhile == True or data.isFor == True:
            data.consola.concatenar("\n goto "+data.etiquetaSalidaCiclo+";")
            data.isWhile = False
            data.etiquetaSalidaCiclo = None
            data.etiquetaRegresoCiclo = None
        else:
            data.errores.insertar("la instruccion break no esta dentro de un ciclo", "", 0, 0, data.texto)
    else:
        op = Operacion()
        resultado = op.ejecutar(expresion, data)
        if data.isLoop == True:
            data.consola.concatenar("\n goto "+data.etiquetaSalidaCiclo+";")
            data.isWhile = False
            data.etiquetaSalidaCiclo = None
            data.etiquetaRegresoCiclo = None
        else:
            data.errores.insertar("la instruccion break no esta dentro de un ciclo", "", resultado.linea, resultado.columna, data.texto)
        
def procesar_continue(data):
    if data.isWhile == True or data.isFor == True:
        data.consola.concatenar("\n goto "+data.etiquetaRegresoCiclo+";")
    else:
        data.errores.insertar("la instruccion continue no esta dentro de un ciclo", "", 0, 0, data.texto)
    
'''def procesar_for(variable, arreglo, inicio, fin, instrucciones, data):
    
    arreglo_temporal = 0
    #aqui manejo el arreglo para el for
    if arreglo == 0:
        temp_value = []
        op = Operacion()
        principio = op.ejecutar(inicio, data)
        final = 0
        if isinstance(fin, ExpresionInicial) or isinstance(fin, ExpresionAritmetica):
            final1 = op.ejecutar(fin, data)
            final = final1.valor
        else:
            simbol = data.ambito.obtenerSimbolo(fin.value, data.ambito.longitud()-1)
            final = len(simbol.valor)
        if principio.tipo == "ENTERO" and isinstance(final, int) :
            for i in range(principio.valor, final, 1):
                temp_value.append(i)
            arreglo_temporal = temp_value
        else:
            temp_ambito = data.ambito.pila[len(data.ambito.pila)-1].nombre
            data.errores.insertar("no se puede recorrer el rango no es numerico ( entero) ", temp_ambito, variable.lineno, variable.lexpos, data.texto)
    else:
        if isinstance(arreglo, list):
            temp_value = []
            op = Operacion()
            for dato1  in arreglo:
                temp_dato = op.ejecutar(dato1, data)
                temp_value.append(temp_dato.valor)
            arreglo_temporal = temp_value
        elif isinstance(arreglo, ExpresionInicial):
            op = Operacion()
            temp_dato = op.ejecutar(arreglo, data)
            if temp_dato.tipo == "CADENA":
                arreglo_temporal = temp_dato.valor
            else:
                temp_ambito = data.ambito.pila[len(data.ambito.pila)-1].nombre
                data.errores.insertar("no hay cadena para convertir a lista de caracteres", temp_ambito, variable.lineno, variable.lexpos, data.texto)
        elif arreglo.type == "ID":
            simbol = data.ambito.obtenerSimbolo(arreglo.value, data.ambito.longitud()-1)
            if isinstance(simbol.valor, list):
                arreglo_temporal = simbol.valor
            elif simbol.tipoDato == "CADENA":
                arreglo_temporal = simbol.valor
            else:
                temp_ambito = data.ambito.pila[len(data.ambito.pila)-1].nombre
                data.errores.insertar("la expresion no es un arreglo", temp_ambito, arreglo.lineno, arreglo.lexpos, data.texto)
    
    if arreglo_temporal == 0:
        temp_ambito = data.ambito.pila[len(data.ambito.pila)-1].nombre
        data.errores.insertar("no hay arreglo para recorrer", temp_ambito, variable.lineno, variable.lexpos, data.texto)
    else:
        from interprete import procesar_instrucciones
        for dato in arreglo_temporal:
            new_ts = TablaSimbolos()
            new_ts.nombre = "For"
            new_ts.isFor = True
            data.ambito.ingresar(new_ts)
            temp_ambito = data.ambito.pila[len(data.ambito.pila)-1].nombre
            data.ambito.ingresarSimbolo(variable.value, dato, "Variable", tipoDatoE(dato), temp_ambito, False, variable.lineno, variable.lexpos, data.texto)
            procesar_instrucciones(instrucciones, data)
            if(data.ambito.pila[data.ambito.longitud()-1].isBreak == True):
                data.ambito.eliminar()
                break
            if(data.ambito.pila[data.ambito.longitud()-1].isContinue == True):
                data.ambito.pila[data.ambito.longitud()-1].isContinue = False
            data.ambito.eliminar()'''

def procesar_declaracion_arreglo(nombre, tamanio, expresiones, data):
    temp = data.ts.obtener(nombre.value, data.pStack, data.pHeap)
    valor = []
    longitud = []
    tt = tamanio_tipo(longitud, tamanio)
    valor = calcular_array(tt[0], tt[1], expresiones[0], data)
    if valor == "error" or tt[1] != temp.tipoDato:
        data.errores.insertar("Hubo un error en la declaracion de la variable", "", nombre.lineno, nombre.lexpos, data.texto)
    else:
        print(temp.dimensiones, temp.tipoDato)
        print(valor)

def procesar_declaracion_arreglo_st(nombre, expresiones, data):
    temp = data.ts.obtener(nombre.value, data.pStack, data.pHeap)
    valor = []
    tt = calcular_tipo_array(expresiones, data)
    valor = calcular_array(None, tt, expresiones[0], data)
    if valor == "error" or tt != temp.tipoDato:
        data.errores.insertar("Hubo un error en la declaracion de la variable", "", nombre.lineno, nombre.lexpos, data.texto)
    else:
        print(temp.dimensiones, temp.tipoDato)
        print(valor)









def procesar_funcion(nombre, tipo, parametros, instrucciones, data):
    #me voy directo a las instrucciones, regresare para los parametros
    if nombre.value == "main":
        simbol = data.ts.obtener(nombre.value, 0, len(data.ts.simbolos))
        data.pStack = data.pHeap
        data.pHeap = simbol.tamanio+1
    data.consola.concatenar("\n")
    data.consola.concatenar("void "+ nombre.value + "() { \n" )
    from interprete import procesar_instrucciones
    procesar_instrucciones(instrucciones, data)
    data.consola.concatenar("\n}")

def tipoDato(dato):
    if dato == "i64": return "ENTERO"
    if dato == "f64": return "DECIMAL"
    if dato == "bool": return "BOOL"
    if dato == "char": return "CARACTER"
    if (dato == "String" or dato == "&str"): return "CADENA"
    else: return dato

#funciones para apoyar la traduccion de arreglos
def calc_dimensiones(arreglo, tamanio):
    tamanio.append(len(arreglo))
    for valor in arreglo:
        if isinstance(valor, list):
            calc_dimensiones(valor, tamanio)
            break
    return tamanio

def tamanio_tipo(longitud, tt):
    longitud.append(tt.tamanio.value)
    if isinstance(tt.tipo, TamanioTipo):
        return tamanio_tipo(longitud, tt.tipo)
    else:
        temp = []
        temp.append(longitud)
        temp.append(tipoDato(tt.tipo.value))
        return temp

def calcular_tipo_array(expresiones, data):
    if isinstance(expresiones, ExpresionInicial):
        op = Operacion()
        dato = op.ejecutar(expresiones, data)
        return dato.tipo
    else:
        for i in expresiones:
            temp = calcular_tipo_array(i, data)
            
        return temp

def calcular_array(base, tipo, expresiones, data):
    array = []
    if isinstance(expresiones, ExpresionInicial):
        op = Operacion()
        dato = op.ejecutar(expresiones, data)
        if dato.tipo == tipo:
            return [dato.valor]
        else:
            return "error"
    elif expresiones == "error":
        return "error"
    else:
        for i in expresiones:
            temp = calcular_array(base, tipo, i, data)
            if temp == "error":
                array = "error"
                return "error"
            else:
                array = array + temp
            
        return array