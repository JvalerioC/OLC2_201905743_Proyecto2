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
    op = Operacion()
    tipo_impresion = ""
    casteo = ""
    tamanio = 1
    dato = op.ejecutar(cadena, data)
    if dato.tipo == "CADENA" and "{:?}" in dato.valor:
        temp = op.ejecutar(expresion, data)
        print(temp.tipoS)
        if temp.tipoS == "Arreglo":
            simbol = data.ts.obtener(expresion.id.value, 0, len(data.ts.simbolos))
            if simbol.tipoDato == "CADENA":
                print("hay que imprimir una cadena")
            else:
                if simbol.tipoDato == "CARACTER":
                    tipo_impresion = 'c'
                    casteo = "(int)"
                elif simbol.tipoDato == "ENTERO":
                    tipo_impresion = "d"
                    casteo = "(int)"
                elif simbol.tipoDato == "DECIMAL":
                    tipo_impresion = "f"
                    casteo = ""
                tr = TraductorExp()
                traductor = tr.traducir_expresion(expresion, data)
                if traductor == "error":
                    return
                if traductor.dimension == None:
                    
                    cadena_temporal = traductor.codigo
                    cadena_temporal += "\n"
                    
                    etiqueta1 = data.obtenerEtiqueta()
                    etiqueta2 = data.obtenerEtiqueta()

                    temporal1 = traductor.direccion
                    temporal2 = data.obtenerTemporal()
                    temporal3 = data.obtenerTemporal()
                    cadena_temporal += temporal2+" = "
                    cadena_temporal += f"heap[(int){temporal1}];"
                    cadena_temporal += "\n"
                    cadena_temporal += temporal3+" = 0;"
                    cadena_temporal += "\n"
                    cadena_temporal += temporal1+" = "+temporal1+" + 1;"
                    cadena_temporal += "\n"
                    cadena_temporal += temporal2+" = "+temporal2+" + "+temporal1+";"
                    cadena_temporal += "\n"
                    cadena_temporal += temporal3+" = "+temporal3+" + "+temporal1+";"
                    cadena_temporal += "\n"
                    cadena_temporal += "printf(\"%c\", 91); "

                    #aqui va el if
                    cadena_temporal += etiqueta1+":\n"
                    cadena_temporal += "if("+temporal2+"=="+temporal3+") goto "+etiqueta2+";\n"
                    cadena_temporal += temporal1+" = heap[(int)"+temporal3+"];\n"
                    cadena_temporal += f"printf(\"%{tipo_impresion}\", {casteo}{temporal1}); "
                    cadena_temporal += "\n"
                    cadena_temporal += "printf(\"%c\", 44);\n"
                    cadena_temporal += temporal3+" = "+temporal3+" + 1;\n"
                    cadena_temporal += "goto "+etiqueta1+";\n"
                    cadena_temporal += etiqueta2+":"
                    cadena_temporal += "\n"
                    cadena_temporal += "printf(\"%c\", 93); "
                    cadena_temporal += "\n"
                    cadena_temporal += "printf(\"%c\", 10);"
                    data.consola.concatenar(cadena_temporal)
                else:
                    etiqueta1 = data.obtenerEtiqueta()
                    etiqueta2 = data.obtenerEtiqueta()

                    cadena_temporal = traductor.codigo
                    temporal1 = traductor.direccion
                    temporal2 = data.obtenerTemporal()
                    temporal3 = data.obtenerTemporal()
                    
                    cadena_temporal += "\n"
                    cadena_temporal += temporal3+" = 0;"
                    cadena_temporal += "\n"
                    cadena_temporal += temporal2+" = "+str(traductor.dimension)+" + "+temporal1+";"
                    cadena_temporal += "\n"
                    cadena_temporal += temporal3+" = "+temporal3+" + "+temporal1+";"
                    cadena_temporal += "\n"
                    cadena_temporal += "printf(\"%c\", 91); "

                    #aqui va el if
                    cadena_temporal += etiqueta1+":\n"
                    cadena_temporal += "if("+temporal2+"=="+temporal3+") goto "+etiqueta2+";\n"
                    cadena_temporal += temporal1+" = heap[(int)"+temporal3+"];\n"
                    cadena_temporal += f"printf(\"%{tipo_impresion}\", {casteo}{temporal1}); "
                    cadena_temporal += "\n"
                    cadena_temporal += "printf(\"%c\", 44);\n"
                    cadena_temporal += temporal3+" = "+temporal3+" + 1;\n"
                    cadena_temporal += "goto "+etiqueta1+";\n"
                    cadena_temporal += etiqueta2+":"
                    cadena_temporal += "\n"
                    cadena_temporal += "printf(\"%c\", 93); "
                    cadena_temporal += "\n"
                    cadena_temporal += "printf(\"%c\", 10);"
                    data.consola.concatenar(cadena_temporal)


        else:
            data.errores.insertar("se esperaba un vector, no se puede imprimir", "", dato.linea, dato.columna, data.texto)
        
    else:
        data.errores.insertar("la cadena no incluye la opcion de imprimir arreglo, o la expresion no es de tipo CADENA", "", dato.linea, dato.columna, data.texto)



def procesar_declaracion1(id, expresion, data):
    op = Operacion()
    dato = op.ejecutar(expresion, data)
    if dato.tipo == "CADENA":
        puntero = data.ts.obtener_puntero_stack(id.value, data.pStack, data.pHeap)
        data.consola.concatenar("\n")
        data.consola.concatenar("stack["+str(puntero)+"] = H;")
        data.consola.concatenar("\n")
        data.consola.concatenar("heap[(int)H] = "+ str(len(expresion.expresion.value))+";")
        data.consola.concatenar("\n")
        data.consola.concatenar("H = H + 1;")
        for caracter in expresion.expresion.value:
            ascii_char = str(ord(caracter))
            data.consola.concatenar("\n")
            data.consola.concatenar("heap[(int)H] = "+ ascii_char+";")
            data.consola.concatenar("\n")
            data.consola.concatenar("H = H + 1;")
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
            data.consola.concatenar("\n")
            data.consola.concatenar("stack["+str(puntero)+"] = H;")
            data.consola.concatenar("\n")
            data.consola.concatenar("heap[(int)H] = "+ str(len(expresion.expresion.value))+";")
            data.consola.concatenar("\n")
            data.consola.concatenar("H = H + 1;")
            for caracter in expresion.expresion.value:
                ascii_char = str(ord(caracter))
                data.consola.concatenar("\n")
                data.consola.concatenar("heap[(int)H] = "+ ascii_char+";")
                data.consola.concatenar("\n")
                data.consola.concatenar("H = H + 1;")
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
        dimension = 1
        for dato in temp.dimensiones:
            dimension = dimension*dato
        cadena_temp = "\n"
        cadena_temp += f"stack[(int){temp.posicionStack}] = H;"
        cadena_temp += "\n"
        cadena_temp += "heap[(int)H] = "+str(dimension)+";"
        cadena_temp += "\n"
        cadena_temp += "H = H + 1;"
        if temp.tipoDato == "CARACTER":
            for dato  in valor:
                cadena_temp += "\n"
                ascii_char = str(ord(dato.value))
                cadena_temp += "heap[(int)H] = "+str(ascii_char)+";"
                cadena_temp += "\n"
                cadena_temp += "H = H + 1;"

        elif temp.tipoDato == "CADENA":
            tamanio_agregado = dimension
            for dato in valor:
                cadena_temp += "\n"
                tem = data.obtenerTemporal()
                cadena_temp += tem+" = H + "+str(tamanio_agregado)+";\n"
                cadena_temp += f"heap[(int)H] = {tem};"
                tamanio_agregado = tamanio_agregado + len(dato)
                cadena_temp += "\n"
                cadena_temp += "H = H + 1;"
            for dato in valor:
                cadena_temp += "\n"
                cadena_temp += "heap[(int)H] = "+str(len(dato))+";"
                cadena_temp += "\n"
                cadena_temp += "H = H + 1;"
                for caracter in dato:
                    cadena_temp += "\n"
                    ascii_char = str(ord(caracter))
                    cadena_temp += "heap[(int)H] = "+ascii_char+";"
                    cadena_temp += "\n"
                    cadena_temp += "H = H + 1;"
            

        else:
            for dato in valor:
                cadena_temp += "\n"
                cadena_temp += "heap[(int)H] = "+str(dato)+";"
                cadena_temp += "\n"
                cadena_temp += "H = H + 1;"
        data.consola.concatenar(cadena_temp)

def procesar_declaracion_arreglo_st(nombre, expresiones, data):
    temp = data.ts.obtener(nombre.value, data.pStack, data.pHeap)
    valor = []
    tt = calcular_tipo_array(expresiones, data)
    valor = calcular_array(None, tt, expresiones[0], data)
    if valor == "error" or tt != temp.tipoDato:
        data.errores.insertar("Hubo un error en la declaracion de la variable", "", nombre.lineno, nombre.lexpos, data.texto)
    else:
        dimension = 1
        for dato in temp.dimensiones:
            dimension = dimension*dato
        cadena_temp = "\n"
        cadena_temp += f"stack[(int){temp.posicionStack}] = H;"
        cadena_temp += "\n"
        cadena_temp += "heap[(int)H] = "+str(dimension)+";"
        cadena_temp += "\n"
        cadena_temp += "H = H + 1;"
        if temp.tipoDato == "CARACTER":
            for dato  in valor:
                cadena_temp += "\n"
                ascii_char = str(ord(dato.value))
                cadena_temp += "heap[(int)H] = "+str(ascii_char)+";"
                cadena_temp += "\n"
                cadena_temp += "H = H + 1;"

        elif temp.tipoDato == "CADENA":
            tamanio_agregado = dimension
            for dato in valor:
                cadena_temp += "\n"
                tem = data.obtenerTemporal()
                cadena_temp += tem+" = H + "+str(tamanio_agregado)+";\n"
                cadena_temp += f"heap[(int)H] = {tem};"
                tamanio_agregado = tamanio_agregado + len(dato)
                cadena_temp += "\n"
                cadena_temp += "H = H + 1;"
            for dato in valor:
                cadena_temp += "\n"
                cadena_temp += "heap[(int)H] = "+str(len(dato))+";"
                cadena_temp += "\n"
                cadena_temp += "H = H + 1;"
                for caracter in dato:
                    cadena_temp += "\n"
                    ascii_char = str(ord(caracter))
                    cadena_temp += "heap[(int)H] = "+ascii_char+";"
                    cadena_temp += "\n"
                    cadena_temp += "H = H + 1;"
            

        else:
            for dato in valor:
                cadena_temp += "\n"
                cadena_temp += "heap[(int)H] = "+str(dato)+";"
                cadena_temp += "\n"
                cadena_temp += "H = H + 1;"
        data.consola.concatenar(cadena_temp)

def procesar_modificar_arreglo(acceso, expresion, data):
    op = Operacion()
    id = acceso[0].value
    a = acceso[1]
    simbol = data.ts.obtener(id, 0, len(data.ts.simbolos))
    if simbol == 0:
        data.errores.insertar("el vector o arreglo a modificar no existe no existe", "", acceso[0].lineno, acceso[0].lexpos, data.texto)
    else:
        if simbol.mutable == True:
            if simbol.tipoSimbolo == "Arreglo":
                dato = op.ejecutar(expresion, data)
                if(dato.tipo == simbol.tipoDato):
                    tr = TraductorExp()
                    traduccion = tr.traducir_expresion(expresion, data)
                    if traduccion == "error":
                        return
                    temp = accesov(a, simbol.dimensiones, data)
                    if temp == "error":
                        print("aqui hay que hacer la comprobacion dinamica")
                        return
                    if dato.tipo == "CADENA":
                        print("arreglo tipo cadena")
                    else:
                        cadena_temporal = '\n'
                        cadena_temporal += traduccion.codigo
                        puntero = simbol.posicionStack
                        cadena_temporal += '\n'
                        temporal = data.obtenerTemporal()
                        cadena_temporal += temporal +" = stack[(int)"+str(puntero)+"];"
                        cadena_temporal += '\n'
                        cadena_temporal += temporal+" = "+temporal+" + "+str(temp+1)+";"
                        cadena_temporal += '\n'
                        cadena_temporal += f"heap[(int){temporal}] = {traduccion.direccion};"
                        cadena_temporal += '\n'
                        data.consola.concatenar(cadena_temporal)
                        #print(a, simbol.dimensiones, temp)
                        #data.ambito.modificarSimbolo(simbol, data.ambito.longitud()-1)
                else:
                    data.errores.insertar("El tipo de la variable no coincide con el tipo de la expresion a asignar", "", acceso[0].lineno, acceso[0].lexpos, data.texto)
            else:
                data.errores.insertar("La variable no es de tipo Arreglo", "", acceso[0].lineno, acceso[0].lexpos, data.texto)
        else:
            data.errores.insertar("el vector o arreglo no se puede modificar, no es mutable", "", acceso[0].lineno, acceso[0].lexpos, data.texto)

def accesov(acceso, dimensiones, data): #este retorna la posicion (row major) del arreglo siempre y cuando cumpla con las dimensiones
    hubo_error = False
    op = Operacion()
    posicion = 1
    value = []
    if len(acceso) == 1:
        dato = op.ejecutar(acceso[0], data)
        if dato.tipo == "ENTERO":
            if dato.valor < dimensiones[0] and dato.valor > -1:
                posicion = dato.valor
            else:
                posicion = "error"
        else:
            data.errores.insertar("no se utilizo un entero para el acceso al arreglo", "", acceso[0].lineno, acceso[0].lexpos, data.texto)
    elif len(acceso) == 2:
        for i in range(len(acceso)):
            dato = op.ejecutar(acceso[i], data)
            if dato.tipo == "ENTERO":
                if dato.valor < dimensiones[i]:
                    hubo_error = False
                    value.append(dato.valor)
                else:
                    hubo_error = True
                    break
            else:
                data.errores.insertar("no se utilizo un entero para el acceso al arreglo", "", acceso[0].lineno, acceso[0].lexpos, data.texto)
        if hubo_error != True:
            posicion = dimensiones[1]*value[0]+value[1]
        else:
            posicion = "error"


    elif len(acceso) == 3:
        for i in range(len(acceso)):
            dato = op.ejecutar(acceso[i], data)
            if dato.tipo == "ENTERO":
                if dato.valor < dimensiones[i]:
                    hubo_error = False
                    value.append(dato.valor)
                else:
                    hubo_error = True
                    break
            else:
                data.errores.insertar("no se utilizo un entero para el acceso al arreglo", "", acceso[0].lineno, acceso[0].lexpos, data.texto)
        if hubo_error != True:
            posicion = dimensiones[2]*dimensiones[1]*value[0]
            posicion += dimensiones[2]*value[1]+value[2]
        else:
            posicion = "error"
    return posicion








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