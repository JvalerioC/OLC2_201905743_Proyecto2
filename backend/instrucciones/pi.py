
def procesar_imprimirV(cadena, expresion, data):
    op = Operacion()
    dato = op.ejecutar(cadena, data)
    if dato.tipo == "CADENA" and "{:?}" in dato.valor:
        temp = op.ejecutar(expresion, data)
        if isinstance(temp.valor, list):
            data.consola.concatenar("> ")
            data.consola.concatenar(str(temp.valor))
            data.consola.concatenar("\n")
        else:
            temp_ambito = data.ambito.pila[len(data.ambito.pila)-1].nombre
            data.errores.insertar("se esperaba un vector, no se puede imprimir", temp_ambito, dato.linea, dato.columna, data.texto)
        
    else:
        temp_ambito = data.ambito.pila[len(data.ambito.pila)-1].nombre
        data.errores.insertar("la cadena no incluye la opcion de imprimir arreglo, o la expresion no es de tipo CADENA", temp_ambito, dato.linea, dato.columna, data.texto)

def procesar_for(variable, arreglo, inicio, fin, instrucciones, data):
    
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
            data.ambito.eliminar()


def procesar_loop(instrucciones, data):
    from interprete import procesar_instrucciones
    new_ts = TablaSimbolos()
    new_ts.nombre = "Loop"
    new_ts.isLoop = True
    data.ambito.ingresar(new_ts)
    while(True):
        procesar_instrucciones(instrucciones, data)
        if(data.ambito.pila[data.ambito.longitud()-1].isBreak == True):
            break
        if(data.ambito.pila[data.ambito.longitud()-1].isContinue == True):
            data.ambito.pila[data.ambito.longitud()-1].isContinue = False
    data.ambito.eliminar()

def procesar_match(expresion, data):
    print()

def procesar_expresion(expresion, data):
    op = Operacion()
    resultado = op.ejecutar(expresion, data)
    data.ambito.pila[data.ambito.longitud()-1].retorno = resultado

def tipoD(dato):
    if dato == "i64": return "ENTERO"
    if dato == "f64": return "DECIMAL"
    if dato == "bool": return "BOOL"
    if dato == "char": return 'CARACTER'
    if dato == "String": return "CADENA"
    if dato == "&str" : return "CADENA"


def procesar_declaracion_arreglo_mutable_st(nombre, expresiones, data):
    temp = data.ambito.pila[data.ambito.longitud()-1].obtener(nombre.value)
    if temp == 0:
        valor = []
        tt = calcular_tipo_array(expresiones, data)
        valor = calcular_array(None, tt, expresiones[0], data)
        if valor == "error":
            temp_ambito = data.ambito.pila[len(data.ambito.pila)-1].nombre
            data.errores.insertar("Hubo un error en la declaracion de la variable", temp_ambito, nombre.lineno, nombre.lexpos, data.texto)
        else:
            temp_ambito = data.ambito.pila[len(data.ambito.pila)-1].nombre
            data.ambito.ingresarSimbolo(nombre.value, valor, "Arreglo", tt, temp_ambito, True, nombre.lineno, nombre.lexpos, data.texto)
    else:
        temp_ambito = data.ambito.pila[len(data.ambito.pila)-1].nombre
        data.errores.insertar("La variable ya existe, no se puede declarar", temp_ambito, nombre.lineno, nombre.lexpos, data.texto)

def procesar_declaracion_arreglo_st(nombre, expresiones, data):
    temp = data.ambito.pila[data.ambito.longitud()-1].obtener(nombre.value)
    if temp == 0:
        valor = []
        tt = calcular_tipo_array(expresiones, data)
        valor = calcular_array(None, tt, expresiones[0], data)
        if valor == "error":
            temp_ambito = data.ambito.pila[len(data.ambito.pila)-1].nombre
            data.errores.insertar("Hubo un error en la declaracion de la variable", temp_ambito, nombre.lineno, nombre.lexpos, data.texto)
        else:
            temp_ambito = data.ambito.pila[len(data.ambito.pila)-1].nombre
            data.ambito.ingresarSimbolo(nombre.value, valor, "Arreglo", tt, temp_ambito, False, nombre.lineno, nombre.lexpos, data.texto)
    else:
        temp_ambito = data.ambito.pila[len(data.ambito.pila)-1].nombre
        data.errores.insertar("La variable ya existe, no se puede declarar", temp_ambito, nombre.lineno, nombre.lexpos, data.texto)

def tamanio_tipo(longitud, tt):
    longitud.append(tt.tamanio.value)
    if isinstance(tt.tipo, TamanioTipo):
        return tamanio_tipo(longitud, tt.tipo)
    else:
        temp = []
        temp.append(longitud)
        temp.append(tipoD(tt.tipo.value))
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
            return dato.valor
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
                array.append(temp)
            
        return array

def procesar_declaracion_vector(nombre, tipo, valor, capacidad, mutable, data):
    is_vector = False
    op = Operacion()
    if tipo == None:
        if isinstance(valor[0], list):
            is_vector = True
        else:
            dato = op.ejecutar(valor[0], data)
            tipo1 = dato.tipo
    else:
        tipo1 = tipo
    
    temp = data.ambito.pila[data.ambito.longitud()-1].obtener(nombre.value)
    if temp == 0:
        if is_vector:
            hubo_error = False
            temp_valor = []
            for v in valor:
                dato = op.ejecutar(v[0], data)
                tipo1 = dato.tipo
                temp_valor1 = []
                for i in v:
                    dato2 = op.ejecutar(i, data)
                    if tipo1 == dato2.tipo:
                        temp_valor1.append(dato2.valor)
                    else:
                        temp_ambito = data.ambito.pila[len(data.ambito.pila)-1].nombre
                        data.errores.insertar("el tipo de dato de la variable no coincide con el tipo de la expresion", temp_ambito, nombre.lineno, nombre.lexpos, data.texto)
                        hubo_error = True
                        break
                if not hubo_error:
                    temp_valor.append(temp_valor1)
                    
                else:
                    break
            if not hubo_error:
                temp_ambito = data.ambito.pila[len(data.ambito.pila)-1].nombre
                data.ambito.ingresarSimboloV(nombre.value, temp_valor, "Vector", tipo1, temp_ambito, mutable, nombre.lineno, nombre.lexpos, data.texto, capacidad, data)
        else:
            temp_valor = []
            hubo_error = False
            for i in valor:
                dato1 = op.ejecutar(i, data)
                if tipo1 == dato1.tipo:
                    temp_valor.append(dato1.valor)
                else:
                    temp_ambito = data.ambito.pila[len(data.ambito.pila)-1].nombre
                    data.errores.insertar("el tipo de dato de la variable no coincide con el tipo de la expresion", temp_ambito, nombre.lineno, nombre.lexpos, data.texto)
                    hubo_error = True
                    break
            if not hubo_error:
                temp_ambito = data.ambito.pila[len(data.ambito.pila)-1].nombre
                data.ambito.ingresarSimboloV(nombre.value, temp_valor, "Vector", tipo1, temp_ambito, mutable, nombre.lineno, nombre.lexpos, data.texto, capacidad, data)
    else:
        temp_ambito = data.ambito.pila[len(data.ambito.pila)-1].nombre
        data.errores.insertar("La variable ya existe, no se puede declarar", temp_ambito, nombre.lineno, nombre.lexpos, data.texto)

def procesar_declaracion_vector2(nombre, tipo, mutable, capacidad, data):
    if tipo.type == "ID":
        temp = data.ambito.pila[data.ambito.longitud()-1].obtener(nombre.value)
        valor = []
        if temp == 0:
            temp_ambito = data.ambito.pila[len(data.ambito.pila)-1].nombre
            data.ambito.ingresarSimboloV(nombre.value, valor, "Vector", tipo.value, temp_ambito, mutable, nombre.lineno, nombre.lexpos, data.texto, capacidad, data)
        else:
            temp_ambito = data.ambito.pila[len(data.ambito.pila)-1].nombre
            data.errores.insertar("La variable ya existe, no se puede declarar", temp_ambito, nombre.lineno, nombre.lexpos, data.texto)
    else:
        temp = data.ambito.pila[data.ambito.longitud()-1].obtener(nombre.value)
        valor = []
        if temp == 0:
            temp_ambito = data.ambito.pila[len(data.ambito.pila)-1].nombre
            data.ambito.ingresarSimboloV(nombre.value, valor, "Vector", tipoD(tipo.value), temp_ambito, mutable, nombre.lineno, nombre.lexpos, data.texto, capacidad, data)
        else:
            temp_ambito = data.ambito.pila[len(data.ambito.pila)-1].nombre
            data.errores.insertar("La variable ya existe, no se puede declarar", temp_ambito, nombre.lineno, nombre.lexpos, data.texto)

def procesar_modificar_arreglo(acceso, expresion, data):
    op = Operacion()
    id = acceso[0].value
    a = acceso[1]
    simbol = data.ambito.obtenerSimbolo(id, data.ambito.longitud()-1)
    if simbol == 0:
        temp_ambito = data.ambito.pila[len(data.ambito.pila)-1].nombre
        data.errores.insertar("el vector o arreglo a modificar no existe no existe", temp_ambito, acceso[0].lineno, acceso[0].lexpos, data.texto)
    else:
        if simbol.mutable == True:
            if simbol.tipoSimbolo == "Arreglo":
                dato = op.ejecutar(expresion, data)
                if(dato.tipo == simbol.tipoDato):
                    temp = accesov(a, simbol.valor, dato.valor, data)
                    if temp == "error":
                        print("es a este al que no entra")
                        temp_ambito = data.ambito.pila[len(data.ambito.pila)-1].nombre
                        data.errores.insertar("No es posible acceder a esta posicion del vector", temp_ambito, acceso[0].lineno, acceso[0].lexpos, data.texto)
                    else:
                        simbol.valor = temp
                        data.ambito.modificarSimbolo(simbol, data.ambito.longitud()-1)
                else:
                    temp_ambito = data.ambito.pila[len(data.ambito.pila)-1].nombre
                    data.errores.insertar("El tipo de la variable no coincide con el tipo de la expresion a asignar", temp_ambito, acceso[0].lineno, acceso[0].lexpos, data.texto)
            else:
                temp_ambito = data.ambito.pila[len(data.ambito.pila)-1].nombre
                data.errores.insertar("La variable no es de tipo Arreglo", temp_ambito, acceso[0].lineno, acceso[0].lexpos, data.texto)
        else:
            temp_ambito = data.ambito.pila[len(data.ambito.pila)-1].nombre
            data.errores.insertar("el vector o arreglo no se puede modificar, no es mutable", temp_ambito, acceso[0].lineno, acceso[0].lexpos, data.texto)

def accesov(acceso, arreglo, dato, data):
    vacio = []
    op = Operacion()
    if len(acceso) >1:
        datito = op.ejecutar(acceso[0], data)
        temp1 = arreglo[datito.valor]
        for i in range(len(arreglo)):
            if i == datito.valor:
                temp2 = accesov(acceso[1:], temp1, dato, data)
                if temp2 == "error":
                    vacio = "error"
                else:
                    vacio.append(temp2)
            else:
                vacio.append(arreglo[i])
        return vacio
    else:
        try:
            datito = op.ejecutar(acceso[0], data)
            arreglo[datito.valor] = dato
            return arreglo
        except:
            return "error"

def vector_push(id, expresion, data):
    if isinstance(expresion, list):
        op = Operacion()
        dato = op.ejecutarStruct(expresion[0], expresion[1], data)
        simbol = data.ambito.obtenerSimbolo(id.value, data.ambito.longitud()-1)
        if simbol == 0:
            temp_ambito = data.ambito.pila[len(data.ambito.pila)-1].nombre
            data.errores.insertar("El vector no existe", temp_ambito, id.lineno, id.lexpos, data.texto)
        else:
            if simbol.mutable and simbol.tipoSimbolo == "Vector":
                if dato.tipo == simbol.tipoDato:
                    temp = simbol.valor
                    temp.append(dato.valor)
                    simbol.valor = temp
                    data.ambito.modificarSimbolo(simbol, data.ambito.longitud()-1)
                else:
                    temp_ambito = data.ambito.pila[len(data.ambito.pila)-1].nombre
                    data.errores.insertar("la expresion a ingresar no es del tipo de vector", temp_ambito, id.lineno, id.lexpos, data.texto)
            else:
                temp_ambito = data.ambito.pila[len(data.ambito.pila)-1].nombre
                data.errores.insertar("el valor del id no es un vector o no se puede modificar, no es mutable", temp_ambito, id.lineno, id.lexpos, data.texto)
    else:
        op = Operacion()
        dato = op.ejecutar(expresion, data)
        simbol = data.ambito.obtenerSimbolo(id.value, data.ambito.longitud()-1)
        if simbol == 0:
            temp_ambito = data.ambito.pila[len(data.ambito.pila)-1].nombre
            data.errores.insertar("El vector no existe", temp_ambito, id.lineno, id.lexpos, data.texto)
        else:
            if simbol.mutable and simbol.tipoSimbolo == "Vector":
                if dato.tipo == simbol.tipoDato:
                    temp = simbol.valor
                    temp.append(dato.valor)
                    simbol.valor = temp
                    data.ambito.modificarSimbolo(simbol, data.ambito.longitud()-1)
                else:
                    temp_ambito = data.ambito.pila[len(data.ambito.pila)-1].nombre
                    data.errores.insertar("la expresion a ingresar no es del tipo de vector", temp_ambito, id.lineno, id.lexpos, data.texto)
            else:
                temp_ambito = data.ambito.pila[len(data.ambito.pila)-1].nombre
                data.errores.insertar("el valor del id no es un vector o no se puede modificar, no es mutable", temp_ambito, id.lineno, id.lexpos, data.texto)

def vector_pushV(id, arreglo, data):
    op = Operacion()
    dato = op.ejecutar(arreglo[0], data)
    tipo1 = dato.tipo
    temp_valor = []
    hubo_error = False

    simbol = data.ambito.obtenerSimbolo(id.value, data.ambito.longitud()-1)
    if simbol == 0:
        temp_ambito = data.ambito.pila[len(data.ambito.pila)-1].nombre
        data.errores.insertar("El vector no existe", temp_ambito, id.lineno, id.lexpos, data.texto)
    else:
        if simbol.mutable and simbol.tipoSimbolo == "Vector":
            if dato.tipo == simbol.tipoDato:

                for i in arreglo:
                    dato1 = op.ejecutar(i, data)
                    if tipo1 == dato1.tipo:
                        temp_valor.append(dato1.valor)
                    else:
                        temp_ambito = data.ambito.pila[len(data.ambito.pila)-1].nombre
                        data.errores.insertar("el tipo de dato de la variable no coincide con el tipo de la expresion", temp_ambito, id.lineno, id.lexpos, data.texto)
                        hubo_error = True
                        break

                if not hubo_error:
                    temp = simbol.valor
                    temp.append(temp_valor)
                    simbol.valor = temp
                    data.ambito.modificarSimbolo(simbol, data.ambito.longitud()-1)
            else:
                temp_ambito = data.ambito.pila[len(data.ambito.pila)-1].nombre
                data.errores.insertar("la expresion a ingresar no es del tipo de vector", temp_ambito, id.lineno, id.lexpos, data.texto)
        else:
            temp_ambito = data.ambito.pila[len(data.ambito.pila)-1].nombre
            data.errores.insertar("el valor del id no es un vector o no se puede modificar, no es mutable", temp_ambito, id.lineno, id.lexpos, data.texto)
   
def vector_insert(id, posicion, expresion, data):
    op = Operacion()
    dato = op.ejecutar(expresion, data)
    simbol = data.ambito.obtenerSimbolo(id.value, data.ambito.longitud()-1)
    if simbol == 0:
        temp_ambito = data.ambito.pila[len(data.ambito.pila)-1].nombre
        data.errores.insertar("El vector no existe", temp_ambito, id.lineno, id.lexpos, data.texto)
    else:
        if simbol.mutable and simbol.tipoSimbolo == "Vector":
            if dato.tipo == simbol.tipoDato:
                temp = simbol.valor
                posicion1 = op.ejecutar(posicion, data)
                if posicion1.tipo == "ENTERO":
                    temp.insert(posicion1.valor, dato.valor)
                    simbol.valor = temp
                    data.ambito.modificarSimbolo(simbol, data.ambito.longitud()-1)
                else:
                    temp_ambito = data.ambito.pila[len(data.ambito.pila)-1].nombre
                    data.errores.insertar("la posicion a insertar no es de tipo numerica", temp_ambito, id.lineno, id.lexpos, data.texto)
            else:
                temp_ambito = data.ambito.pila[len(data.ambito.pila)-1].nombre
                data.errores.insertar("la expresion a ingresar no es del tipo de vector", temp_ambito, id.lineno, id.lexpos, data.texto)
        else:
            temp_ambito = data.ambito.pila[len(data.ambito.pila)-1].nombre
            data.errores.insertar("el valor del id no es un vector o no se puede modificar, no es mutable", temp_ambito, id.lineno, id.lexpos, data.texto)

def vector_remove(id, posicion, data):
    simbol = data.ambito.obtenerSimbolo(id.value, data.ambito.longitud()-1)
    op = Operacion()
    if simbol == 0:
        temp_ambito = data.ambito.pila[len(data.ambito.pila)-1].nombre
        data.errores.insertar("El vector no existe", temp_ambito, id.lineno, id.lexpos, data.texto)
    else:
        if simbol.mutable and simbol.tipoSimbolo == "Vector":
            temp = simbol.valor
            posicion1 = op.ejecutar(posicion, data)
            if posicion1.tipo == "ENTERO":
                temp.pop(posicion1.valor)
                simbol.valor = temp
                data.ambito.modificarSimbolo(simbol, data.ambito.longitud()-1)
            else:
                temp_ambito = data.ambito.pila[len(data.ambito.pila)-1].nombre
                data.errores.insertar("la posicion a insertar no es de tipo numerica", temp_ambito, id.lineno, id.lexpos, data.texto)
        else:
            temp_ambito = data.ambito.pila[len(data.ambito.pila)-1].nombre
            data.errores.insertar("el valor del id no es un vector o no se puede modificar, no es mutable", temp_ambito, id.lineno, id.lexpos, data.texto)

def llamada_funcion(id, parametros, data):
    buscar = data.funciones.obtener(id.value)
    if buscar == 0:
        temp_ambito = data.ambito.pila[len(data.ambito.pila)-1].nombre
        data.errores.insertar("la funcion no existe existe", temp_ambito, id.lineno, id.lexpos, data.texto)
    else:
        if parametros == None:
            from interprete import procesar_instrucciones
            new_ts = TablaSimbolos()
            new_ts.nombre = buscar.nombre
            data.ambito.ingresar(new_ts)
            procesar_instrucciones(buscar.instrucciones, data)
            data.ambito.eliminar()
        else:
            from interprete import procesar_instrucciones
            new_ts = TablaSimbolos()
            new_ts.nombre = buscar.nombre
            new_ts.isFuncion = True
            
            op = Operacion()
            hubo_error = False
            for i in range(len(parametros)):
                tipo_param = 0
                if isinstance(parametros[i], ExpresionInicial) and parametros[i].expresion.type == "ID":
                    param = data.ambito.obtenerSimboloLlamada(parametros[i].expresion.value, data.ambito.longitud()-1)
                    tipo_param = param.tipoDato
                else:
                    param = op.ejecutar(parametros[i], data)
                    tipo_param = param.tipo
                
                if (tipoDato(buscar.parametros[i].tipo.value)) == tipo_param:
                    if buscar.parametros[i].isReferencia == "V":
                        tipoS = "Vector"
                    elif buscar.parametros[i].isReferencia == "A":
                        tipoS = "Arreglo"
                    else:
                        tipoS = "Variable"
                    
                    columnaF = find_column(data.texto, id.lexpos)
                    temp_ambito = buscar.nombre
                    simbol = Simbolo(buscar.parametros[i].id.value, param.valor, tipoS, tipo_param, temp_ambito, True, id.lineno, columnaF)
                    new_ts.ingresar(simbol)
                else:
                    temp_ambito = data.ambito.pila[len(data.ambito.pila)-1].nombre
                    data.errores.insertar("un parametro no coincide con el tipo de los parametros de la funcion", temp_ambito, id.lineno, id.lexpos, data.texto)
                    hubo_error = True
                    break
            if hubo_error:
                return
            else:
                data.ambito.ingresar(new_ts)
                procesar_instrucciones(buscar.instrucciones, data)
                data.ambito.eliminar()

def llamada_funcionDB(id, parametros, lfunciones, data):
    buscar = lfunciones.obtener(id.value)
    if buscar == 0:
        temp_ambito = data.ambito.pila[len(data.ambito.pila)-1].nombre
        data.errores.insertar("la funcion no existe existe", temp_ambito, id.lineno, id.lexpos, data.texto)
    else:
        if parametros == None:
            from interprete import procesar_instrucciones
            new_ts = TablaSimbolos()
            new_ts.nombre = buscar.nombre
            data.ambito.ingresar(new_ts)
            procesar_instrucciones(buscar.instrucciones, data)
            data.ambito.eliminar()
        else:
            from interprete import procesar_instrucciones
            new_ts = TablaSimbolos()
            new_ts.nombre = buscar.nombre
            new_ts.isFuncion = True
            
            op = Operacion()
            hubo_error = False
            for i in range(len(parametros)):
                tipo_param = 0
                if isinstance(parametros[i], ExpresionInicial) and parametros[i].expresion.type == "ID":
                    param = data.ambito.obtenerSimboloLlamada(parametros[i].expresion.value, data.ambito.longitud()-1)
                    tipo_param = param.tipoDato
                else:
                    param = op.ejecutar(parametros[i], data)
                    tipo_param = param.tipo
                
                if (tipoDato(buscar.parametros[i].tipo.value)) == tipo_param:
                    if buscar.parametros[i].isReferencia == "V":
                        tipoS = "Vector"
                    elif buscar.parametros[i].isReferencia == "A":
                        tipoS = "Arreglo"
                    else:
                        tipoS = "Variable"
                    
                    columnaF = find_column(data.texto, id.lexpos)
                    temp_ambito = buscar.nombre
                    simbol = Simbolo(buscar.parametros[i].id.value, param.valor, tipoS, tipo_param, temp_ambito, True, id.lineno, columnaF)
                    new_ts.ingresar(simbol)
                else:
                    temp_ambito = data.ambito.pila[len(data.ambito.pila)-1].nombre
                    data.errores.insertar("un parametro no coincide con el tipo de los parametros de la funcion", temp_ambito, id.lineno, id.lexpos, data.texto)
                    hubo_error = True
                    break
            if hubo_error:
                return
            else:
                data.ambito.ingresar(new_ts)
                procesar_instrucciones(buscar.instrucciones, data)
                data.ambito.eliminar()

def procesar_return(expresion, data):
    if expresion == None:
        temp = False
        for i in range(data.ambito.longitud()-1, -1, -1):
            if data.ambito.pila[i].isFuncion == True:
                data.ambito.pila[i].isReturn = True
                temp = True
                break
        if temp == False:
            temp_ambito = data.ambito.pila[len(data.ambito.pila)-1].nombre
            data.errores.insertar("la instruccion return no esta dentro de una funcion", temp_ambito, 0, 0, data.texto)
    elif isinstance(expresion, list):
        temp = False
        op = Operacion()
        #print(expresion[0], expresion[1])
        dato = op.ejecutarStruct(expresion[0], expresion[1], data)
        dato.tipoS = "Struct"
        #print(dato.valor, dato.tipo)
        for i in range(data.ambito.longitud()-1, -1, -1):
            if data.ambito.pila[i].isFuncion == True:
                data.ambito.pila[i].isReturn = True
                data.ambito.pila[i].retorno = dato
                temp = True
                break
        if temp == False:
            temp_ambito = data.ambito.pila[len(data.ambito.pila)-1].nombre
            data.errores.insertar("la instruccion return no esta dentro de una funcion", temp_ambito, resultado.linea, resultado.columna, data.texto)

    else:
        op = Operacion()
        temp = False
        resultado = op.ejecutar(expresion, data)
        for i in range(data.ambito.longitud()-1, -1, -1):
            if data.ambito.pila[i].isFuncion == True:
                data.ambito.pila[i].isReturn = True
                data.ambito.pila[i].retorno = resultado
                temp = True
                break
        if temp == False:
            temp_ambito = data.ambito.pila[len(data.ambito.pila)-1].nombre
            data.errores.insertar("la instruccion return no esta dentro de una funcion", temp_ambito, resultado.linea, resultado.columna, data.texto)
    
def procesar_declaracion_struct(id, idStruct, campos, mutable, data):
    #print(id, idStruct, campos, mutable)
    por_si_las_moscas = data.structs
    buscar = 0
    if len(data.structs.structs) == 0 and len(data.modulos.modulos) != 0:
        temp_mods = data.modulos.modulos
        for mod in temp_mods:
            if len(mod.st.structs) == 0 and len(mod.mod.modulos) != 0:
                temp_mods1 = mod.mod.modulos
                for mod1 in temp_mods1:
                    buscar = mod1.st.obtener(idStruct.value)
                    if buscar != 0:
                        break
                
            else:
                buscar = mod1.st.obtener(idStruct.value)
                if buscar != 0:
                        break
    
    if buscar == 0:
        buscar = data.structs.obtener(idStruct.value)
        
    if buscar == 0:
        temp_ambito = data.ambito.pila[len(data.ambito.pila)-1].nombre
        data.errores.insertar("El struct no existe", temp_ambito, id.lineno, id.lexpos, data.texto)
        return
    
    if len(buscar.campos) == len(campos):
        atributos = {}
        op = Operacion()
        hubo_error = False
        for i in range(len(buscar.campos)):
            if buscar.campos[i].nombre.value == campos[i].nombre.value:
                if isinstance(buscar.campos[i].tipo, TamanioTipo) and isinstance(campos[i].valor, list):
                    temp_a = []
                    for j in campos[i].valor[0]:
                        dato1 = op.ejecutar(j, data)

                        if dato1.tipo == tipoDato(buscar.campos[i].tipo.tipo.value):
                            temp_a.append(dato1.valor)

                        else:
                            temp_ambito = data.ambito.pila[len(data.ambito.pila)-1].nombre
                            data.errores.insertar("un dato del array no coinside con el tipo del array", temp_ambito, campos[i].nombre.lineno, campos[i].nombre.lexpos, data.texto)
                            hubo_error = True
                            break
                    if not hubo_error:
                        hubo_error = False
                        atributos[campos[i].nombre.value] = temp_a
                        
                elif buscar.campos[i].tipo.type == "ID":
                    from structsG import Campo2
                    if isinstance(campos[i].valor, Campo2):
                        dato = op.ejecutarStruct(campos[i].valor.nombre, campos[i].valor.valor, data)
                        atributos[campos[i].nombre.value] = dato.valor
                    else:
                        simbol = data.ambito.obtenerSimbolo(campos[i].valor.expresion.value, data.ambito.longitud()-1)
                        if simbol == 0 or simbol == None or simbol == "error":
                            temp_ambito = data.ambito.pila[len(data.ambito.pila)-1].nombre
                            data.errores.insertar("la variable no existe", temp_ambito, campos[i].nombre.lineno, campos[i].nombre.lexpos, data.texto)
                            hubo_error = True
                        else:
                            if simbol.tipoDato == buscar.campos[i].tipo.value:
                                atributos[campos[i].nombre.value] = simbol.valor
                            else:
                                temp_ambito = data.ambito.pila[len(data.ambito.pila)-1].nombre
                                data.errores.insertar("el tipo de la variable no coincide con el tipo del atributo del struct", temp_ambito, campos[i].nombre.lineno, campos[i].nombre.lexpos, data.texto)
                                hubo_error = True
                else:
                    dato = op.ejecutar(campos[i].valor, data)
                
                    if dato.tipo == tipoDato(buscar.campos[i].tipo.value):
                        atributos[campos[i].nombre.value] = dato.valor
                    else:
                        temp_ambito = data.ambito.pila[len(data.ambito.pila)-1].nombre
                        data.errores.insertar("el tipo del atributo en la declaracion no coincide con el tipo del atributo del struct", temp_ambito, campos[i].nombre.lineno, campos[i].nombre.lexpos, data.texto)
                        hubo_error = True
                        break
            else:
                temp_ambito = data.ambito.pila[len(data.ambito.pila)-1].nombre
                data.errores.insertar("el nombre del atributo en la declaracion no coincide con el nombre del atributo del struct ", temp_ambito, campos[i].nombre.lineno, campos[i].nombre.lexpos, data.texto)
                hubo_error = True
                break
        if not hubo_error and len(atributos) == len(campos):
            temp = data.ambito.pila[data.ambito.longitud()-1].obtener(id.value)
            if temp == 0:

                temp_ambito = data.ambito.pila[len(data.ambito.pila)-1].nombre
                data.ambito.ingresarSimbolo(id.value, atributos, "Struct", idStruct.value, temp_ambito, mutable, id.lineno, id.lexpos, data.texto)
            else:
                temp_ambito = data.ambito.pila[len(data.ambito.pila)-1].nombre
                data.errores.insertar("no se puede declarar el struct la variable ya existe", temp_ambito, id.lineno, id.lexpos, data.texto)
        else:
            temp_ambito = data.ambito.pila[len(data.ambito.pila)-1].nombre
            data.errores.insertar("la cantidad de atributos no cumple", temp_ambito, id.lineno, id.lexpos, data.texto)
    else:
        temp_ambito = data.ambito.pila[len(data.ambito.pila)-1].nombre
        data.errores.insertar("la cantidad de atributos declarados no coincide con la cantidad de atributos del struct", temp_ambito, id.lineno, id.lexpos, data.texto)
    
def procesar_modificar_struct(id_atributo, expresion, data):
    #print(id_atributo, expresion)
    print("este es una modificacion")
   
def procesar_declaracion_vectorT(id, listamod, data):
    tipo = listamod[len(listamod)-1]
    listamod = listamod[:len(listamod)-1]
    if len(listamod) > 1:
        buscar = data.modulos.obtener(listamod[0].value)
        retorno = procesar_instrucciones_mod(buscar.instrucciones, buscar, data)
        
        #print(len(retorno.mod.modulos), len(retorno.fn.funciones), len(retorno.st.structs), "aqui tiene que ser el 100")
        buscar1 = None
        for mod in buscar.mod.modulos:
            if mod.nombre == listamod[1].value:
                buscar1 = mod
                break
        retorno = None
        if buscar1 != None:
            retorno = procesar_instrucciones_mod(buscar1.instrucciones, buscar1, data)
            
            #print(len(retorno.mod.modulos), len(retorno.fn.funciones), len(retorno.st.structs), "aqui tiene que ser el 051")
        if retorno != None:
            #buscar.mod.modulos.append(buscar1)
            data.modulos.actualizar(buscar)

    else:
        buscar = data.modulos.obtener(listamod[0].value)
        retorno = procesar_instrucciones_mod(buscar.instrucciones, buscar, data)
        data.modulos.actualizar(retorno)
    
    temp = data.ambito.pila[data.ambito.longitud()-1].obtener(id.value)
    valor = []
    values = listamod
    if temp == 0:
        temp_ambito = data.ambito.pila[len(data.ambito.pila)-1].nombre
        data.ambito.ingresarSimboloV2(id.value, valor, "Vector", tipo.value, temp_ambito, True, id.lineno, id.lexpos, data.texto, None, values, data)
    else:
        temp_ambito = data.ambito.pila[len(data.ambito.pila)-1].nombre
        data.errores.insertar("La variable ya existe, no se puede declarar", temp_ambito, id.lineno, id.lexpos, data.texto)

def procesar_asignacion_tabla(nombre, tipo, mutable, capacidad, data):
    op = Operacion()
    simbol = data.ambito.obtenerSimbolo(nombre.value, data.ambito.longitud()-1)
    if simbol != 0:
        temp = op.ejecutar(capacidad, data)
        simbol.capacidad = temp.valor
        data.ambito.modificarSimbolo(simbol, data.ambito.longitud()-1)
    else:
        print("algo salio mal en el inicio de la tabla")

def procesar_instrucciones_mod(instrucciones, buscar, data):
    from instrucciones.instrucciones import Funcion, Modulo, Struct
    buscar = buscar
    for inst in instrucciones:
        if isinstance(inst, Funcion) :
            buscar.fn.insertar(inst.nombre.value, inst.tipo, inst.parametros, inst.instrucciones, inst.nombre.lineno, inst.nombre.lexpos, data.texto)
        elif isinstance(inst, Modulo) :
            buscar.mod.insertar(inst.nombre.value, inst.instrucciones, inst.nombre.lineno, inst.nombre.lexpos, data.texto)
        elif isinstance(inst, Struct) :
            buscar.st.insertar(inst.nombre.value, inst.campos, inst.nombre.lineno, inst.nombre.lexpos, data.texto)
        else:
            print("no se que paso, pero esto no debe estar aqui")
    return buscar

def modificacion_atributoDB(id, posicion, atributo, expresion, data):
    op = Operacion()
    simbol = data.ambito.obtenerSimbolo(id.value, data.ambito.longitud()-1)
    if simbol == 0:
        temp_ambito = data.ambito.pila[len(data.ambito.pila)-1].nombre
        data.errores.insertar("el vector o arreglo a modificar no existe no existe", temp_ambito, id.lineno, id.lexpos, data.texto)
    else:
        if simbol.mutable == True:
            if simbol.tipoSimbolo == "Vector":
                dato = op.ejecutar(posicion, data)
                dato1 = op.ejecutar(expresion, data)
                if(dato.tipo == "ENTERO"):
                    try:
                        simbol.valor[dato.valor][atributo.value] = dato1.valor
                        data.ambito.modificarSimbolo(simbol, data.ambito.longitud()-1)
                    except:
                        print("es a este al que no entra")
                        temp_ambito = data.ambito.pila[len(data.ambito.pila)-1].nombre
                        data.errores.insertar("No es posible acceder a esta posicion del vector", temp_ambito, id.lineno, id.lexpos, data.texto)
                    
                else:
                    temp_ambito = data.ambito.pila[len(data.ambito.pila)-1].nombre
                    data.errores.insertar("el indice del vector no es de tipo entero", temp_ambito, id.lineno, id.lexpos, data.texto)
            else:
                temp_ambito = data.ambito.pila[len(data.ambito.pila)-1].nombre
                data.errores.insertar("La variable no es de tipo Vector", temp_ambito, id.lineno, id.lexpos, data.texto)
        else:
            temp_ambito = data.ambito.pila[len(data.ambito.pila)-1].nombre
            data.errores.insertar("el vector o arreglo no se puede modificar, no es mutable", temp_ambito, id.lineno, id.lexpos, data.texto)

#funciones para verificaciones
def tipoDato(dato):
    if dato == "i64": return "ENTERO"
    if dato == "f64": return "DECIMAL"
    if dato == "bool": return "BOOL"
    if dato == "char": return "CARACTER"
    if (dato == "String" or dato == "&str"): return "CADENA"
    else: return dato



# aqui empezare con las instrucciones globales (funciones, structs, modulos)

def procesar_struct_global(nombre, campos, data):
    #print(nombre.lineno)
    data.structs.insertar(nombre.value, campos, nombre.lineno, nombre.lexpos, data.texto)

def procesar_modulo_global(nombre, instrucciones, data):
    data.modulos.insertar(nombre.value, instrucciones, nombre.lineno, nombre.lexpos, data.texto)
 

